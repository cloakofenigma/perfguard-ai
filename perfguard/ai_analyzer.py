"""
PerfGuard AI Analyzer
Uses Google Gemini to analyze code changes and predict performance risks
"""
import os
import json
import time
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from config import config
from logger import get_logger
from prompts import get_prompt

logger = get_logger(__name__)


class AIAnalyzer:
    """Analyzes code changes using Google Gemini AI"""

    def __init__(self):
        # Initialize Gemini
        if not config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")

        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.gemini_model = genai.GenerativeModel(config.GEMINI_MODEL)
        logger.info(f"Google Gemini initialized ({config.GEMINI_MODEL})")

        self.max_tokens = config.MAX_TOKENS

    def _sanitize_text(self, text: str) -> str:
        """
        Sanitize ANY text to handle Unicode characters properly
        Used for prompts, error messages, and anything that might be logged
        Uses aggressive ASCII-only encoding to prevent any encoding errors
        """
        if not isinstance(text, str):
            text = str(text)

        try:
            # First, replace common Unicode characters with ASCII equivalents
            replacements = {
                '\u201c': '"',  # Left double quote
                '\u201d': '"',  # Right double quote
                '\u2018': "'",  # Left single quote
                '\u2019': "'",  # Right single quote
                '\u2013': '-',  # En dash
                '\u2014': '--', # Em dash
                '\u2026': '...', # Ellipsis
                '\u00a0': ' ',  # Non-breaking space
                '\u2022': '*',  # Bullet point
            }
            sanitized = text
            for unicode_char, ascii_char in replacements.items():
                sanitized = sanitized.replace(unicode_char, ascii_char)

            # Then aggressively encode to ASCII, replacing any remaining non-ASCII chars
            # This ensures NO Unicode characters can cause encoding errors
            sanitized = sanitized.encode('ascii', errors='replace').decode('ascii')

            return sanitized
        except Exception:
            # If even sanitization fails, use most aggressive approach
            try:
                return text.encode('ascii', errors='ignore').decode('ascii')
            except:
                return "Error: Could not sanitize text"

    def _sanitize_prompt(self, prompt: str) -> str:
        """Alias for _sanitize_text for backward compatibility"""
        return self._sanitize_text(prompt)

    def _call_gemini(self, prompt: str, max_retries: int) -> str:
        """Call Google Gemini API with retries and safety settings"""
        # Sanitize prompt to handle Unicode characters
        sanitized_prompt = self._sanitize_prompt(prompt)

        last_error = None
        for attempt in range(max_retries):
            try:
                logger.info(f"Calling Google Gemini API (attempt {attempt + 1}/{max_retries})...")

                # Configure generation settings
                generation_config = {
                    "max_output_tokens": self.max_tokens,
                    "temperature": 0.1,  # Low temperature for consistent analysis
                }

                # Configure safety settings to be permissive for code analysis
                safety_settings = [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE",
                    },
                ]

                response = self.gemini_model.generate_content(
                    sanitized_prompt,
                    generation_config=generation_config,
                    safety_settings=safety_settings
                )

                # Check if response was blocked or has no content
                if not response.candidates:
                    logger.warning("No candidates returned by Gemini API")
                    raise Exception("Response blocked: no candidates returned")

                # Check finish_reason
                candidate = response.candidates[0]
                finish_reason = candidate.finish_reason

                # finish_reason values: 0=UNSPECIFIED, 1=STOP(success), 2=MAX_TOKENS, 3=SAFETY, 4=RECITATION, 5=OTHER
                if finish_reason != 1:  # 1 = STOP (normal completion)
                    reason_map = {
                        0: "UNSPECIFIED",
                        2: "MAX_TOKENS (content too long)",
                        3: "SAFETY (blocked by safety filters)",
                        4: "RECITATION (blocked due to recitation)",
                        5: "OTHER"
                    }
                    reason_text = reason_map.get(finish_reason, f"Unknown ({finish_reason})")
                    logger.warning(f"Response finished with reason: {reason_text}")

                    # For MAX_TOKENS, we might still have partial content
                    if finish_reason == 2 and hasattr(candidate.content, 'parts') and candidate.content.parts:
                        content = candidate.content.parts[0].text
                        logger.info(f"✅ Received partial response from Gemini ({len(content)} chars) - MAX_TOKENS reached")
                        return content

                    raise Exception(f"Response blocked or incomplete: {reason_text}")

                content = response.text
                logger.info(f"✅ Received response from Gemini ({len(content)} chars)")
                return content

            except Exception as e:
                last_error = e
                error_msg = self._sanitize_text(str(e))

                # Check if it's a rate limit or quota error
                error_str = str(e).lower()
                if 'rate' in error_str or 'quota' in error_str:
                    logger.warning(f"Gemini API error (attempt {attempt + 1}): {error_msg}")
                    if attempt < max_retries - 1:
                        time.sleep(config.API_RETRY_DELAY * (attempt + 1))
                elif 'max_tokens' in error_str or 'finish_reason' in error_str:
                    logger.warning(f"Gemini content issue (attempt {attempt + 1}): {error_msg}")
                    # Don't retry for content issues, break immediately
                    break
                else:
                    logger.error(f"Unexpected Gemini error: {error_msg}")
                    if attempt < max_retries - 1:
                        time.sleep(config.API_RETRY_DELAY)

        error_msg = self._sanitize_text(str(last_error)) if last_error else "Unknown error"
        raise Exception(f"Gemini API failed after {max_retries} attempts: {error_msg}")

    def _call_llm(self, prompt: str, max_retries: int = None) -> str:
        """
        Call Gemini LLM API with retries

        Args:
            prompt: The prompt to send
            max_retries: Maximum retry attempts (defaults to config)

        Returns:
            Response text from LLM

        Raises:
            Exception: If API call fails
        """
        if max_retries is None:
            max_retries = config.API_RETRY_ATTEMPTS

        return self._call_gemini(prompt, max_retries)

    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract JSON from Gemini's response (handles markdown code blocks and various formats)

        Args:
            response_text: Raw response from Gemini

        Returns:
            Parsed JSON dictionary
        """
        if not response_text or not response_text.strip():
            logger.error("Empty response from Gemini")
            return self._get_default_response()

        # Try direct JSON parse first
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass

        # Try extracting from markdown code blocks
        try:
            # Look for ```json blocks
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                if end != -1:
                    json_str = response_text[start:end].strip()
                    return json.loads(json_str)

            # Look for generic ``` blocks
            elif "```" in response_text:
                start = response_text.find("```") + 3
                # Skip language identifier if present
                newline_pos = response_text.find('\n', start)
                if newline_pos != -1:
                    start = newline_pos + 1
                end = response_text.find("```", start)
                if end != -1:
                    json_str = response_text[start:end].strip()
                    return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON in code block failed to parse: {e}")
        except Exception as e:
            logger.warning(f"Error extracting from code block: {e}")

        # Try finding JSON object with balanced braces
        try:
            start = response_text.find('{')
            if start != -1:
                # Find matching closing brace
                brace_count = 0
                end = start
                for i in range(start, len(response_text)):
                    if response_text[i] == '{':
                        brace_count += 1
                    elif response_text[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end = i + 1
                            break

                if end > start:
                    json_str = response_text[start:end]
                    return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON extraction with brace matching failed: {e}")
        except Exception as e:
            logger.warning(f"Error finding JSON structure: {e}")

        # Last resort: log full response and return default
        logger.error("Could not extract JSON from response after all attempts")
        logger.error(f"Full response text:\n{response_text[:1000]}")

        return self._get_default_response()

    def _get_default_response(self) -> Dict[str, Any]:
        """Return default response structure when parsing fails"""
        return {
            "risk_score": 0.5,  # Default medium risk
            "critical_paths": [],
            "suggested_benchmarks": ["test_general_performance"],
            "reasoning": "Could not parse AI response - defaulting to medium risk",
            "suggestions": ["Review changes manually", "Run comprehensive performance tests"]
        }

    def _smart_truncate_diff(self, diff: str, max_chars: int = 5000) -> str:
        """
        Intelligently truncate diff to focus on actual code changes

        Args:
            diff: Full git diff
            max_chars: Maximum characters to return

        Returns:
            Truncated diff focusing on code changes
        """
        if len(diff) <= max_chars:
            return diff

        # Try to extract just the meaningful changes (added/removed lines)
        lines = diff.split('\n')
        important_lines = []
        char_count = 0

        for line in lines:
            # Include file headers and actual changes
            if (line.startswith('diff --git') or
                line.startswith('+++') or
                line.startswith('---') or
                line.startswith('+') or
                line.startswith('-') or
                line.startswith('@@')):

                line_len = len(line) + 1  # +1 for newline
                if char_count + line_len > max_chars:
                    break
                important_lines.append(line)
                char_count += line_len

        truncated = '\n'.join(important_lines)
        logger.info(f"Truncated diff from {len(diff)} to {len(truncated)} chars")
        return truncated

    def analyze_diff(self, diff: str, changed_files: List[str] = None) -> Dict[str, Any]:
        """
        Analyze git diff for performance risks

        Args:
            diff: Git diff string
            changed_files: List of changed file paths

        Returns:
            Dictionary with analysis results
        """
        logger.info("Analyzing code diff with AI...")

        if not diff or diff.strip() == "":
            logger.warning("Empty diff provided")
            return {
                "risk_score": 0.0,
                "critical_paths": [],
                "suggested_benchmarks": [],
                "reasoning": "No changes detected",
                "suggestions": []
            }

        try:
            # Intelligently truncate diff to focus on important changes
            truncated_diff = self._smart_truncate_diff(diff, max_chars=5000)

            # Use the diff analysis prompt
            prompt = get_prompt("diff_analysis", diff=truncated_diff)

            # Call Gemini with retry
            response_text = self._call_llm(prompt)

            # Extract JSON
            result = self._extract_json_from_response(response_text)

            # Validate and sanitize result
            result = self._validate_analysis_result(result)

            logger.info(f"AI Analysis: risk={result['risk_score']}, paths={len(result['critical_paths'])}")

            return result

        except Exception as e:
            error_msg = self._sanitize_text(str(e))
            logger.error(f"Error during AI analysis: {error_msg}", exc_info=True)
            # Return safe default
            return {
                "risk_score": 0.5,
                "critical_paths": changed_files or [],
                "suggested_benchmarks": ["test_general_performance"],
                "reasoning": f"AI analysis failed: {str(e)}",
                "suggestions": ["Manual review required", "Run full test suite"]
            }

    def refine_score(
        self,
        raw_score: float,
        metrics: Dict[str, Any],
        risk_score: float
    ) -> Dict[str, Any]:
        """
        Use AI to refine the raw performance score

        Args:
            raw_score: Calculated raw score
            metrics: Collected metrics
            risk_score: AI risk assessment

        Returns:
            Dictionary with adjusted score and justification
        """
        logger.info("Refining score with AI...")

        try:
            prompt = get_prompt(
                "score_refinement",
                raw_score=raw_score,
                metrics=json.dumps(metrics, indent=2),
                risk_score=risk_score
            )

            response_text = self._call_llm(prompt)
            result = self._extract_json_from_response(response_text)

            adjusted_score = result.get("adjusted_score", raw_score)
            justification = result.get("justification", "Score refined by AI")

            logger.info(f"Score refined: {raw_score} -> {adjusted_score}")

            return {
                "adjusted_score": adjusted_score,
                "justification": justification
            }

        except Exception as e:
            error_msg = self._sanitize_text(str(e))
            logger.error(f"Error refining score: {error_msg}")
            return {
                "adjusted_score": raw_score,
                "justification": "AI refinement unavailable"
            }

    def assess_overall_risk(
        self,
        changed_files: List[str],
        performance_history: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Assess overall PR risk based on changed files and history

        Args:
            changed_files: List of changed file paths
            performance_history: Historical performance data

        Returns:
            Dictionary with risk assessment
        """
        logger.info("Assessing overall PR risk...")

        try:
            prompt = get_prompt(
                "risk_assessment",
                files="\n".join(changed_files),
                history=json.dumps(performance_history or {}, indent=2)
            )

            response_text = self._call_llm(prompt)
            result = self._extract_json_from_response(response_text)

            return {
                "overall_risk": result.get("overall_risk", "medium"),
                "perf_impact": result.get("perf_impact", "Unknown"),
                "details": result
            }

        except Exception as e:
            error_msg = self._sanitize_text(str(e))
            logger.error(f"Error assessing risk: {error_msg}")
            return {
                "overall_risk": "medium",
                "perf_impact": "Unknown",
                "details": {}
            }

    def _validate_analysis_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize AI analysis result"""

        # Ensure required fields exist
        validated = {
            "risk_score": float(result.get("risk_score", 0.5)),
            "critical_paths": result.get("critical_paths", []),
            "suggested_benchmarks": result.get("suggested_benchmarks", []),
            "reasoning": result.get("reasoning", "No reasoning provided"),
            "suggestions": result.get("suggestions", [])
        }

        # Clamp risk score to 0-1
        validated["risk_score"] = max(0.0, min(1.0, validated["risk_score"]))

        # Ensure lists
        if not isinstance(validated["critical_paths"], list):
            validated["critical_paths"] = []
        if not isinstance(validated["suggested_benchmarks"], list):
            validated["suggested_benchmarks"] = []
        if not isinstance(validated["suggestions"], list):
            if isinstance(validated["suggestions"], str):
                validated["suggestions"] = [validated["suggestions"]]
            else:
                validated["suggestions"] = []

        return validated


# Convenience function for backwards compatibility
def analyze_diff_with_ai(diff: str) -> Dict[str, Any]:
    """
    Convenience function to analyze diff

    Args:
        diff: Git diff string

    Returns:
        Analysis results dictionary
    """
    analyzer = AIAnalyzer()
    return analyzer.analyze_diff(diff)
