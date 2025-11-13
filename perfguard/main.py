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


def get_git_diff(base_ref: str = "HEAD~1") -> str:
    """
    Get git diff from base reference

    Args:
        base_ref: Base git reference (default: HEAD~1)

    Returns:
        Git diff as string
    """
    try:
        logger.info(f"Getting git diff from {base_ref}...")
        result = subprocess.run(
            ["git", "diff", base_ref],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',  # Replace invalid characters instead of failing
            check=True,
            timeout=30
        )
        diff = result.stdout

        if not diff or diff.strip() == "":
            logger.warning(f"No changes detected compared to {base_ref}")
            # Try different base
            result = subprocess.run(
                ["git", "diff", "HEAD^"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30
            )
            diff = result.stdout

        logger.info(f"Git diff retrieved ({len(diff)} chars)")
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
    Get list of changed files

    Args:
        base_ref: Base git reference

    Returns:
        List of changed file paths
    """
    try:
        logger.info("Getting list of changed files...")
        result = subprocess.run(
            ["git", "diff", "--name-only", base_ref],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=True,
            timeout=30
        )

        files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
        logger.info(f"Found {len(files)} changed files")
        return files

    except Exception as e:
        logger.error(f"Error getting changed files: {e}")
        return []


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
*Powered by Claude 3.5 Sonnet*
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

        # Step 1: Get git diff and changed files
        diff = get_git_diff()
        changed_files = get_changed_files()

        if not diff and not changed_files:
            logger.warning("No changes detected, nothing to analyze")
            # Create minimal report
            score_data = {
                "performance_score": 100,
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
            # Step 2: AI Analysis
            logger.info("Step 1/3: Running AI analysis...")
            analyzer = AIAnalyzer()
            ai_response = analyzer.analyze_diff(diff, changed_files)

            # Step 3: Collect performance metrics
            logger.info("Step 2/3: Collecting performance metrics...")
            metrics = collect_metrics(
                suggested_benchmarks=ai_response.get("suggested_benchmarks", []),
                changed_files=changed_files
            )

            # Step 4: Calculate final score
            logger.info("Step 3/3: Calculating performance score...")
            score_data = calculate_score(metrics, ai_response)

        # Step 5: Save results
        logger.info("Saving results...")

        # Save JSON score
        with open(config.RESULTS_PATH, 'w') as f:
            json.dump(score_data, f, indent=2)
        logger.info(f"Score saved to {config.RESULTS_PATH}")

        # Generate and save markdown report
        report = generate_markdown_report(score_data, ai_response)
        with open(config.REPORT_PATH, 'w') as f:
            f.write(report)
        logger.info(f"Report saved to {config.REPORT_PATH}")

        # Step 6: Print summary
        logger.info("=" * 60)
        logger.info(f"FINAL SCORE: {score_data['performance_score']:.1f}/100")
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
