"""
PerfGuard AI Analyzer
Uses Claude 3.5 Sonnet or GPT-4 to analyze code changes and predict performance risks
"""
import os
import json
import time
from typing import Dict, Any, List, Optional
from anthropic import Anthropic, APIError, APITimeoutError, RateLimitError
from openai import OpenAI, APIError as OpenAIAPIError, RateLimitError as OpenAIRateLimitError
from config import config
from logger import get_logger
from prompts import get_prompt

logger = get_logger(__name__)


class AIAnalyzer:
    """Analyzes code changes using Claude AI or OpenAI GPT (with automatic fallback)"""

    def __init__(self):
        # Initialize available providers
        self.anthropic_client = None
        self.openai_client = None

        if config.ANTHROPIC_API_KEY:
            self.anthropic_client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
            logger.info("Anthropic Claude initialized")

        if config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
            logger.info("OpenAI GPT initialized")

        if not self.anthropic_client and not self.openai_client:
            raise ValueError("At least one AI API key (ANTHROPIC_API_KEY or OPENAI_API_KEY) is required")

        self.max_tokens = config.MAX_TOKENS

    def _sanitize_prompt(self, prompt: str) -> str:
        """
        Sanitize prompt to handle Unicode characters properly
        Ensures the prompt can be safely encoded and sent to AI APIs
        Uses aggressive ASCII-only encoding to prevent any encoding errors
        """
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
            sanitized = prompt
            for unicode_char, ascii_char in replacements.items():
                sanitized = sanitized.replace(unicode_char, ascii_char)

            # Then aggressively encode to ASCII, replacing any remaining non-ASCII chars
            # This ensures NO Unicode characters can cause encoding errors
            sanitized = sanitized.encode('ascii', errors='replace').decode('ascii')

            return sanitized
        except Exception as e:
            # If even sanitization fails, use most aggressive approach
            try:
                return prompt.encode('ascii', errors='ignore').decode('ascii')
            except:
                return "Error: Could not sanitize prompt"

    def _call_anthropic(self, prompt: str, max_retries: int) -> Optional[str]:
        """Try calling Anthropic Claude API with retries"""
        if not self.anthropic_client:
            return None

        # Sanitize prompt to handle Unicode characters
        sanitized_prompt = self._sanitize_prompt(prompt)

        last_error = None
        for attempt in range(max_retries):
            try:
                logger.info(f"Calling Claude API (attempt {attempt + 1}/{max_retries})...")

                response = self.anthropic_client.messages.create(
                    model=config.CLAUDE_MODEL,
                    max_tokens=self.max_tokens,
                    messages=[{"role": "user", "content": sanitized_prompt}],
                    timeout=config.API_TIMEOUT
                )

                content = response.content[0].text
                logger.info(f"✅ Received response from Claude ({len(content)} chars)")
                return content

            except (RateLimitError, APITimeoutError, APIError) as e:
                last_error = e
                logger.warning(f"Claude API error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(config.API_RETRY_DELAY * (attempt + 1))

            except Exception as e:
                last_error = e
                logger.error(f"Unexpected Claude error: {e}")
                break

        logger.error(f"❌ Claude API failed after {max_retries} attempts: {last_error}")
        return None

    def _call_openai(self, prompt: str, max_retries: int) -> Optional[str]:
        """Try calling OpenAI GPT API with retries"""
        if not self.openai_client:
            return None

        # Sanitize prompt to handle Unicode characters
        sanitized_prompt = self._sanitize_prompt(prompt)

        last_error = None
        for attempt in range(max_retries):
            try:
                logger.info(f"Calling OpenAI GPT API (attempt {attempt + 1}/{max_retries})...")

                response = self.openai_client.chat.completions.create(
                    model=config.OPENAI_MODEL,
                    messages=[{"role": "user", "content": sanitized_prompt}],
                    max_tokens=self.max_tokens,
                    timeout=config.API_TIMEOUT
                )

                content = response.choices[0].message.content
                logger.info(f"✅ Received response from OpenAI ({len(content)} chars)")
                return content

            except (OpenAIRateLimitError, OpenAIAPIError) as e:
                last_error = e
                logger.warning(f"OpenAI API error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(config.API_RETRY_DELAY * (attempt + 1))

            except Exception as e:
                last_error = e
                logger.error(f"Unexpected OpenAI error: {e}")
                break

        logger.error(f"❌ OpenAI API failed after {max_retries} attempts: {last_error}")
        return None

    def _call_llm_with_fallback(self, prompt: str, max_retries: int = None) -> str:
        """
        Call LLM API with automatic fallback to backup provider

        Tries providers in order: Anthropic -> OpenAI

        Args:
            prompt: The prompt to send
            max_retries: Maximum retry attempts per provider (defaults to config)

        Returns:
            Response text from LLM

        Raises:
            Exception: If all providers fail
        """
        if max_retries is None:
            max_retries = config.API_RETRY_ATTEMPTS

        # Try Anthropic first
        if self.anthropic_client:
            logger.info("🔄 Trying Anthropic Claude...")
            result = self._call_anthropic(prompt, max_retries)
            if result:
                return result

        # Fallback to OpenAI
        if self.openai_client:
            logger.info("🔄 Falling back to OpenAI GPT...")
            result = self._call_openai(prompt, max_retries)
            if result:
                return result

        # All providers failed
        raise Exception(f"All LLM providers failed after {max_retries} attempts each")

    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract JSON from Claude's response (handles markdown code blocks)

        Args:
            response_text: Raw response from Claude

        Returns:
            Parsed JSON dictionary
        """
        try:
            # Try direct JSON parse first
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass

        # Try extracting from code blocks
        try:
            # Look for ```json or ``` blocks
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
                return json.loads(json_str)
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
                return json.loads(json_str)
        except:
            pass

        # Try finding JSON-like structure
        try:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response_text[start:end]
                return json.loads(json_str)
        except:
            pass

        # Last resort: return structured error
        logger.error("Could not extract JSON from response")
        logger.debug(f"Response text: {response_text[:500]}")

        return {
            "error": "Failed to parse JSON from response",
            "raw_response": response_text[:500],
            "risk_score": 0.5,  # Default medium risk
            "critical_paths": [],
            "suggested_benchmarks": [],
            "reasoning": "Could not parse AI response",
            "suggestions": ["Review changes manually"]
        }

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
            # Use the diff analysis prompt
            prompt = get_prompt("diff_analysis", diff=diff[:10000])  # Limit diff size

            # Call Claude with retry
            response_text = self._call_llm_with_fallback(prompt)

            # Extract JSON
            result = self._extract_json_from_response(response_text)

            # Validate and sanitize result
            result = self._validate_analysis_result(result)

            logger.info(f"AI Analysis: risk={result['risk_score']}, paths={len(result['critical_paths'])}")

            return result

        except Exception as e:
            logger.error(f"Error during AI analysis: {e}", exc_info=True)
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

            response_text = self._call_llm_with_fallback(prompt)
            result = self._extract_json_from_response(response_text)

            adjusted_score = result.get("adjusted_score", raw_score)
            justification = result.get("justification", "Score refined by AI")

            logger.info(f"Score refined: {raw_score} -> {adjusted_score}")

            return {
                "adjusted_score": adjusted_score,
                "justification": justification
            }

        except Exception as e:
            logger.error(f"Error refining score: {e}")
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

            response_text = self._call_llm_with_fallback(prompt)
            result = self._extract_json_from_response(response_text)

            return {
                "overall_risk": result.get("overall_risk", "medium"),
                "perf_impact": result.get("perf_impact", "Unknown"),
                "details": result
            }

        except Exception as e:
            logger.error(f"Error assessing risk: {e}")
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
def analyze_diff_with_claude(diff: str) -> Dict[str, Any]:
    """
    Convenience function to analyze diff

    Args:
        diff: Git diff string

    Returns:
        Analysis results dictionary
    """
    analyzer = AIAnalyzer()
    return analyzer.analyze_diff(diff)
