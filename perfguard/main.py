#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PerfGuard AI Main Entry Point
Orchestrates the full performance analysis workflow
"""
import os
import sys
import json
import subprocess
import time
from typing import List, Dict, Any
from pathlib import Path
import locale

# Force UTF-8 encoding for entire script
if sys.version_info >= (3, 7):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
else:
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, errors='replace')

# Set locale to UTF-8
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    pass  # Ignore if locale not available

from config import config
from logger import get_logger
from ai_analyzer import AIAnalyzer
from metrics_collector import collect_metrics
from rules_engine import calculate_score

logger = get_logger(__name__)

# Dashboard output paths
DASHBOARD_PUBLIC_DIR = Path(__file__).parent.parent / "dashboard" / "public"
DASHBOARD_REPORT_PATH = DASHBOARD_PUBLIC_DIR / "report.json"
BASELINE_SCORE_PATH = DASHBOARD_PUBLIC_DIR / "baseline_score.json"


def get_git_diff(base_ref: str = "HEAD~1") -> str:
    """
    Get git diff from base reference for APPLICATION_PATH only

    Args:
        base_ref: Base git reference (default: HEAD~1)

    Returns:
        Git diff as string (scoped to APPLICATION_PATH only)
    """
    try:
        app_path = config.APPLICATION_PATH
        logger.info(f"Getting git diff from {base_ref} for {app_path}/ only...")

        # Use flags to optimize diff size:
        # --no-color: Remove ANSI color codes
        # --no-ext-diff: Don't use external diff tools
        # --unified=2: Reduce context lines from 3 to 2
        # -- {app_path}/: Only analyze application directory
        result = subprocess.run(
            ["git", "diff", "--no-color", "--no-ext-diff", "--unified=2", base_ref, "--", f"{app_path}/"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',  # Replace invalid characters instead of failing
            check=True,
            timeout=30
        )
        diff = result.stdout

        if not diff or diff.strip() == "":
            logger.warning(f"No changes detected in {app_path}/ compared to {base_ref}")
            # Try different base
            result = subprocess.run(
                ["git", "diff", "--no-color", "--no-ext-diff", "--unified=2", "HEAD^", "--", f"{app_path}/"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30
            )
            diff = result.stdout

        # Log size warning if diff is very large
        if len(diff) > 1000000:  # > 1MB
            logger.warning(f"Git diff is very large ({len(diff)} chars). This may contain binary or generated files.")
            logger.warning("Consider using .gitattributes to mark binary files or excluding them from analysis.")

        logger.info(f"Git diff retrieved for {app_path}/ ({len(diff)} chars)")
        return diff

    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {e}")
        logger.error(f"stderr: {e.stderr}")
        return ""
    except Exception as e:
        logger.error(f"Error getting git diff: {e}")
        return ""


def get_changed_files(base_ref: str = "HEAD~1") -> List[str]:
    """
    Get list of changed files in APPLICATION_PATH only

    Args:
        base_ref: Base git reference

    Returns:
        List of changed file paths (scoped to APPLICATION_PATH)
    """
    try:
        app_path = config.APPLICATION_PATH
        logger.info(f"Getting list of changed files in {app_path}/...")
        result = subprocess.run(
            ["git", "diff", "--name-only", base_ref, "--", f"{app_path}/"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=True,
            timeout=30
        )

        files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
        logger.info(f"Found {len(files)} changed files in {app_path}/")
        return files

    except Exception as e:
        logger.error(f"Error getting changed files: {e}")
        return []


def load_baseline_score() -> float:
    """
    Load previous baseline score from dashboard

    Returns:
        Previous score or 100.0 if no baseline exists
    """
    try:
        if BASELINE_SCORE_PATH.exists():
            with open(BASELINE_SCORE_PATH, 'r') as f:
                data = json.load(f)
                score = data.get("score", 100.0)
                logger.info(f"Loaded baseline score: {score}")
                return score
        else:
            logger.info("No baseline score found, using default: 100.0")
            return 100.0
    except Exception as e:
        logger.warning(f"Error loading baseline score: {e}, using default: 100.0")
        return 100.0


def save_baseline_score(score: float):
    """
    Save current score as baseline for next run

    Args:
        score: Current performance score
    """
    try:
        DASHBOARD_PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
        with open(BASELINE_SCORE_PATH, 'w') as f:
            json.dump({
                "score": score,
                "timestamp": time.time(),
                "date": time.strftime("%Y-%m-%d %H:%M:%S")
            }, f, indent=2)
        logger.info(f"Saved baseline score: {score}")
    except Exception as e:
        logger.error(f"Error saving baseline score: {e}")


def calculate_delta_score(ai_response: Dict[str, Any], changed_files: List[str]) -> float:
    """
    Calculate a score specifically for the new code changes

    Args:
        ai_response: AI analysis of changes
        changed_files: List of changed file paths

    Returns:
        Score (0-100) for just the new changes
    """
    try:
        # Start with base score
        delta_score = 100.0

        # Factor 1: AI Risk Score (0-1) -> Higher risk = lower score
        risk_score = ai_response.get("risk_score", 0.5)
        risk_penalty = risk_score * 40  # Max 40 point penalty
        delta_score -= risk_penalty

        # Factor 2: Number of critical paths identified
        critical_paths = ai_response.get("critical_paths", [])
        if len(critical_paths) > 0:
            path_penalty = min(len(critical_paths) * 5, 20)  # Max 20 point penalty
            delta_score -= path_penalty

        # Factor 3: File count and complexity (estimate)
        if len(changed_files) > 10:
            complexity_penalty = min((len(changed_files) - 10) * 2, 20)  # Max 20 point penalty
            delta_score -= complexity_penalty

        # Clamp to 0-100 range
        delta_score = max(0.0, min(100.0, delta_score))

        logger.info(f"Delta score for new changes: {delta_score:.1f}")
        return delta_score

    except Exception as e:
        logger.error(f"Error calculating delta score: {e}")
        return 50.0  # Default to medium score


def sanitize_output(text: str) -> str:
    """Sanitize output to prevent injection"""
    # Basic sanitization - remove potentially dangerous characters
    dangerous_patterns = ['<script', 'javascript:', 'onerror=', 'onclick=']
    sanitized = text

    for pattern in dangerous_patterns:
        if pattern.lower() in sanitized.lower():
            logger.warning(f"Potentially dangerous pattern detected: {pattern}")
            sanitized = sanitized.replace(pattern, '[REMOVED]')

    return sanitized


def generate_markdown_report(score_data: Dict[str, Any], ai_response: Dict[str, Any]) -> str:
    """
    Generate markdown report for PR comment

    Args:
        score_data: Score calculation results
        ai_response: AI analysis results

    Returns:
        Formatted markdown report
    """
    score = score_data.get("performance_score", 0)
    verdict = score_data.get("verdict", "UNKNOWN")
    block = score_data.get("block_merge", True)

    # Determine emoji
    if score >= 90:
        emoji = "🌟"
    elif score >= 80:
        emoji = "✅"
    elif score >= 70:
        emoji = "⚠️"
    else:
        emoji = "🚫"

    # Build report
    report = f"""## {emoji} PerfGuard AI Report

**Score: {score:.1f} / 100**
**Verdict: {verdict}**
**Status: {'❌ MERGE BLOCKED' if block else '✅ APPROVED'}**

---

### 📊 Performance Metrics Breakdown

"""

    # Add individual scores
    details = score_data.get("details", {})
    for metric, data in details.items():
        metric_score = data.get("score", 0)
        current = data.get("current", 0)
        baseline = data.get("baseline", 0)
        change = data.get("change_percent", 0)

        status_icon = "✅" if metric_score >= 80 else "⚠️" if metric_score >= 70 else "❌"

        report += f"- **{metric.replace('_', ' ').title()}**: {status_icon} {metric_score:.1f}/100\n"
        if baseline > 0:
            report += f"  - Current: `{current:.4f}` | Baseline: `{baseline:.4f}` | Change: `{change:+.2f}%`\n"

    # AI Analysis section
    report += f"\n### 🤖 AI Analysis\n\n"
    report += f"**Risk Score**: {ai_response.get('risk_score', 0):.2f}/1.00\n\n"

    reasoning = sanitize_output(ai_response.get("reasoning", "No analysis available"))
    report += f"**Reasoning**: {reasoning}\n\n"

    # Critical paths
    critical_paths = ai_response.get("critical_paths", [])
    if critical_paths:
        report += f"**Critical Paths Identified**:\n"
        for path in critical_paths[:5]:  # Limit to 5
            report += f"- `{path}`\n"
        report += "\n"

    # Suggestions
    suggestions = ai_response.get("suggestions", [])
    if suggestions:
        report += f"### 💡 Suggestions for Improvement\n\n"
        for i, suggestion in enumerate(suggestions[:5], 1):
            clean_suggestion = sanitize_output(str(suggestion))
            report += f"{i}. {clean_suggestion}\n"
        report += "\n"

    # Footer
    report += f"""---

*Generated by [PerfGuard AI](https://github.com/cloakofenigma/perfguard-ai)*
*Powered by Google Gemini 2.5 Pro*
"""

    return report


def main():
    """Main execution flow"""
    try:
        logger.info("=" * 60)
        logger.info("PerfGuard AI - Performance Analysis Starting")
        logger.info("=" * 60)

        # Validate configuration
        try:
            config.validate()
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            sys.exit(1)

        # Step 1: Load baseline score
        logger.info("Step 0: Loading baseline score...")
        previous_score = load_baseline_score()

        # Step 2: Get git diff and changed files
        diff = get_git_diff()
        changed_files = get_changed_files()

        if not diff and not changed_files:
            logger.warning("No changes detected, nothing to analyze")
            # Create minimal report
            score_data = {
                "performance_score": 100,
                "previous_score": previous_score,
                "current_score": 100,
                "delta_score": 100,
                "verdict": "PASS",
                "block_merge": False,
                "scores": {},
                "details": {},
                "metrics": {},
                "ai_analysis": {
                    "risk_score": 0,
                    "critical_paths": [],
                    "reasoning": "No changes detected",
                    "suggestions": []
                }
            }
            ai_response = score_data["ai_analysis"]
        else:
            # Step 3: AI Analysis
            logger.info("Step 1/4: Running AI analysis...")
            analyzer = AIAnalyzer()
            ai_response = analyzer.analyze_diff(diff, changed_files)

            # Step 4: Collect performance metrics
            logger.info("Step 2/4: Collecting performance metrics...")
            metrics = collect_metrics(
                suggested_benchmarks=ai_response.get("suggested_benchmarks", []),
                changed_files=changed_files
            )

            # Step 5: Calculate final score
            logger.info("Step 3/4: Calculating performance score...")
            score_data = calculate_score(metrics, ai_response)

            # Step 6: Calculate delta score for new changes
            logger.info("Step 4/4: Calculating delta score for new changes...")
            delta_score = calculate_delta_score(ai_response, changed_files)

            # Add three-score tracking to score_data
            current_score = score_data["performance_score"]
            score_data["previous_score"] = previous_score
            score_data["current_score"] = current_score
            score_data["delta_score"] = delta_score

        # Step 7: Save results
        logger.info("Saving results...")

        # Save JSON score to root directory (backward compatibility)
        with open(config.RESULTS_PATH, 'w') as f:
            json.dump(score_data, f, indent=2)
        logger.info(f"Score saved to {config.RESULTS_PATH}")

        # Save JSON report to dashboard/public directory
        try:
            DASHBOARD_PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
            with open(DASHBOARD_REPORT_PATH, 'w') as f:
                json.dump(score_data, f, indent=2)
            logger.info(f"Dashboard report saved to {DASHBOARD_REPORT_PATH}")
        except Exception as e:
            logger.error(f"Error saving dashboard report: {e}")

        # Generate and save markdown report
        report = generate_markdown_report(score_data, ai_response)
        with open(config.REPORT_PATH, 'w') as f:
            f.write(report)
        logger.info(f"Report saved to {config.REPORT_PATH}")

        # Save current score as baseline for next run
        save_baseline_score(score_data["current_score"])

        # Step 8: Print summary
        logger.info("=" * 60)
        logger.info("PERFORMANCE SCORE SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Previous Overall Score:  {score_data.get('previous_score', 0):.1f}/100")
        logger.info(f"Current Overall Score:   {score_data.get('current_score', 0):.1f}/100")
        logger.info(f"New Code Changes Score:  {score_data.get('delta_score', 0):.1f}/100")
        logger.info(f"")
        logger.info(f"VERDICT: {score_data['verdict']}")
        logger.info(f"MERGE: {'BLOCKED' if score_data['block_merge'] else 'APPROVED'}")
        logger.info("=" * 60)

        # Exit with appropriate code
        if score_data["block_merge"]:
            logger.error("Performance score below threshold. Exiting with error code.")
            sys.exit(1)
        else:
            logger.info("Performance check passed!")
            sys.exit(0)

    except KeyboardInterrupt:
        logger.warning("Process interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Fatal error in main execution: {e}", exc_info=True)

        # Create error report
        error_report = f"""## 🚨 PerfGuard AI Error

An error occurred during performance analysis:

```
{str(e)}
```

**Action Required**: Manual review needed

---

*Generated by [PerfGuard AI](https://github.com/cloakofenigma/perfguard-ai)*
"""

        try:
            with open(config.REPORT_PATH, 'w') as f:
                f.write(error_report)

            error_score = {
                "performance_score": 0,
                "verdict": "ERROR",
                "block_merge": True,
                "error": str(e)
            }
            with open(config.RESULTS_PATH, 'w') as f:
                json.dump(error_score, f, indent=2)
        except:
            pass

        sys.exit(1)


if __name__ == '__main__':
    main()
