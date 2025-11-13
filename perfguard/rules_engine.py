"""
PerfGuard AI Rules Engine
Calculates performance scores based on weighted metrics
"""
import json
from typing import Dict, Any
from config import config
from logger import get_logger

logger = get_logger(__name__)


def calculate_metric_score(
    metric_name: str,
    current_value: float,
    baseline_value: float,
    threshold: float,
    higher_is_better: bool = False
) -> float:
    """
    Calculate score for a single metric (0-100)

    Args:
        metric_name: Name of the metric
        current_value: Current measured value
        baseline_value: Baseline value for comparison
        threshold: Allowed threshold (e.g., 0.15 for 15%)
        higher_is_better: If True, higher values = better score
    """
    if baseline_value == 0:
        logger.warning(f"{metric_name}: Baseline is 0, using absolute value")
        return 100 if current_value == 0 else 50

    # Calculate percentage change
    change_percent = (current_value - baseline_value) / baseline_value

    # For metrics where higher is worse (time, memory, cpu, io)
    if not higher_is_better:
        if change_percent <= 0:
            # Improvement - give bonus points
            score = 100 + abs(change_percent) * 100
            return min(score, 120)  # Cap at 120
        elif change_percent <= threshold:
            # Within acceptable threshold
            score = 100 - (change_percent / threshold) * 20
            return max(score, 80)
        else:
            # Regression beyond threshold - penalize heavily
            excess = (change_percent - threshold) / threshold
            penalty = 30 + (excess * 50)
            score = 100 - penalty
            return max(score, 0)
    else:
        # For metrics where higher is better (rare)
        if change_percent >= 0:
            score = 100 + (change_percent * 100)
            return min(score, 120)
        else:
            score = 100 + (change_percent * 100)
            return max(score, 0)


def calculate_complexity_score(
    current_complexity: int,
    baseline_complexity: int,
    threshold_delta: int = 2
) -> float:
    """Calculate score based on code complexity change"""
    delta = current_complexity - baseline_complexity

    if delta <= 0:
        # Complexity reduced - good!
        return 100
    elif delta <= threshold_delta:
        # Within acceptable range
        score = 100 - (delta / threshold_delta) * 20
        return max(score, 80)
    else:
        # Complexity increased too much
        excess = delta - threshold_delta
        penalty = 30 + (excess * 10)
        score = 100 - penalty
        return max(score, 0)


def calculate_ai_risk_score(ai_risk: float) -> float:
    """
    Convert AI risk (0-1) to score (0-100)
    High risk = low score
    """
    # Invert the risk: risk 0 = score 100, risk 1 = score 0
    base_score = (1 - ai_risk) * 100

    # Apply threshold penalty
    threshold = config.get_threshold("ai_risk_threshold")
    if ai_risk > threshold:
        # High risk - penalize
        excess = (ai_risk - threshold) / (1 - threshold)
        penalty = excess * 30
        base_score -= penalty

    return max(base_score, 0)


def calculate_score(metrics: Dict[str, Any], ai_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate final performance score using weighted metrics

    Args:
        metrics: Dictionary containing current and baseline metrics
        ai_response: AI analysis response with risk assessment

    Returns:
        Dictionary with score, verdict, and detailed breakdown
    """
    logger.info("Calculating performance score...")

    scores = {}
    details = {}

    try:
        # 1. Execution Time Score (30%)
        if "execution_time" in metrics:
            exec_data = metrics["execution_time"]
            scores["execution_time"] = calculate_metric_score(
                "execution_time",
                exec_data.get("current", 0),
                exec_data.get("baseline", 0),
                config.get_threshold("execution_time"),
                higher_is_better=False
            )
            details["execution_time"] = {
                "score": scores["execution_time"],
                "current": exec_data.get("current", 0),
                "baseline": exec_data.get("baseline", 0),
                "change_percent": exec_data.get("change_percent", 0)
            }
            logger.info(f"Execution Time Score: {scores['execution_time']:.1f}")
        else:
            scores["execution_time"] = 100
            logger.warning("No execution time metrics available")

        # 2. Memory RSS Score (20%)
        if "memory_rss" in metrics:
            mem_data = metrics["memory_rss"]
            scores["memory_rss"] = calculate_metric_score(
                "memory_rss",
                mem_data.get("current", 0),
                mem_data.get("baseline", 0),
                config.get_threshold("memory_rss"),
                higher_is_better=False
            )
            details["memory_rss"] = {
                "score": scores["memory_rss"],
                "current": mem_data.get("current", 0),
                "baseline": mem_data.get("baseline", 0),
                "change_percent": mem_data.get("change_percent", 0)
            }
            logger.info(f"Memory RSS Score: {scores['memory_rss']:.1f}")
        else:
            scores["memory_rss"] = 100
            logger.warning("No memory metrics available")

        # 3. CPU Utilization Score (15%)
        if "cpu_utilization" in metrics:
            cpu_data = metrics["cpu_utilization"]
            scores["cpu_utilization"] = calculate_metric_score(
                "cpu_utilization",
                cpu_data.get("current", 0),
                cpu_data.get("baseline", 0),
                config.get_threshold("cpu_utilization"),
                higher_is_better=False
            )
            details["cpu_utilization"] = {
                "score": scores["cpu_utilization"],
                "current": cpu_data.get("current", 0),
                "baseline": cpu_data.get("baseline", 0),
                "change_percent": cpu_data.get("change_percent", 0)
            }
            logger.info(f"CPU Utilization Score: {scores['cpu_utilization']:.1f}")
        else:
            scores["cpu_utilization"] = 100
            logger.warning("No CPU metrics available")

        # 4. I/O Latency Score (15%)
        if "io_latency" in metrics:
            io_data = metrics["io_latency"]
            scores["io_latency"] = calculate_metric_score(
                "io_latency",
                io_data.get("current", 0),
                io_data.get("baseline", 0),
                config.get_threshold("io_latency"),
                higher_is_better=False
            )
            details["io_latency"] = {
                "score": scores["io_latency"],
                "current": io_data.get("current", 0),
                "baseline": io_data.get("baseline", 0),
                "change_percent": io_data.get("change_percent", 0)
            }
            logger.info(f"I/O Latency Score: {scores['io_latency']:.1f}")
        else:
            scores["io_latency"] = 100
            logger.warning("No I/O latency metrics available")

        # 5. Code Complexity Score (10%)
        if "complexity" in metrics:
            comp_data = metrics["complexity"]
            scores["complexity"] = calculate_complexity_score(
                comp_data.get("current", 0),
                comp_data.get("baseline", 0),
                config.get_threshold("complexity_delta")
            )
            details["complexity"] = {
                "score": scores["complexity"],
                "current": comp_data.get("current", 0),
                "baseline": comp_data.get("baseline", 0),
                "delta": comp_data.get("delta", 0)
            }
            logger.info(f"Complexity Score: {scores['complexity']:.1f}")
        else:
            scores["complexity"] = 100
            logger.warning("No complexity metrics available")

        # 6. AI Risk Score (10%)
        ai_risk = ai_response.get("risk_score", 0)
        scores["ai_risk"] = calculate_ai_risk_score(ai_risk)
        details["ai_risk"] = {
            "score": scores["ai_risk"],
            "risk_level": ai_risk,
            "threshold": config.get_threshold("ai_risk_threshold")
        }
        logger.info(f"AI Risk Score: {scores['ai_risk']:.1f} (risk={ai_risk})")

        # Calculate weighted final score
        raw_score = (
            config.get_weight("execution_time") * scores.get("execution_time", 100) / 100 +
            config.get_weight("memory_rss") * scores.get("memory_rss", 100) / 100 +
            config.get_weight("cpu_utilization") * scores.get("cpu_utilization", 100) / 100 +
            config.get_weight("io_latency") * scores.get("io_latency", 100) / 100 +
            config.get_weight("complexity") * scores.get("complexity", 100) / 100 +
            config.get_weight("ai_risk") * scores.get("ai_risk", 100) / 100
        )

        # Round to specified precision
        final_score = round(raw_score, config.SCORE_PRECISION)

        # Determine verdict
        block_merge = final_score < config.MIN_PASSING_SCORE
        if final_score >= 90:
            verdict = "EXCELLENT"
        elif final_score >= config.MIN_PASSING_SCORE:
            verdict = "PASS"
        elif final_score >= 70:
            verdict = "WARNING"
        else:
            verdict = "BLOCKED"

        logger.info(f"Final Score: {final_score}/100 - {verdict}")

        return {
            "performance_score": final_score,
            "verdict": verdict,
            "block_merge": block_merge,
            "scores": scores,
            "details": details,
            "metrics": metrics,
            "ai_analysis": {
                "risk_score": ai_risk,
                "critical_paths": ai_response.get("critical_paths", []),
                "reasoning": ai_response.get("reasoning", ""),
                "suggestions": ai_response.get("suggestions", [])
            }
        }

    except Exception as e:
        logger.error(f"Error calculating score: {e}", exc_info=True)
        # Return a safe default
        return {
            "performance_score": 0,
            "verdict": "ERROR",
            "block_merge": True,
            "error": str(e),
            "scores": {},
            "details": {},
            "metrics": metrics,
            "ai_analysis": ai_response
        }
