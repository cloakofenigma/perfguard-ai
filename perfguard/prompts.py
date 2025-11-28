PROMPTS = {
    "diff_analysis": """
You are a performance engineer analyzing code changes for performance risks.

Code diff:
{diff}

Analyze the diff and provide your assessment in STRICT JSON format (no markdown, no extra text).

Required JSON structure:
{{
  "risk_score": <float between 0 and 1, where 1 is highest risk>,
  "critical_paths": [<list of file paths that may impact performance>],
  "suggested_benchmarks": [<list of 3-5 test names to benchmark>],
  "reasoning": "<brief explanation of performance concerns>",
  "suggestions": [<list of 3-5 actionable suggestions>]
}}

IMPORTANT: Return ONLY the JSON object, nothing else. No markdown code blocks, no explanations before or after.
    """,

    "score_refinement": """
Refine this raw perf score (0-100) based on metrics and context.

Raw score: {raw_score}
Metrics: {metrics}
AI risk: {risk_score}

Adjust for regressions/improvements. Be strict (>15% regression = -20 pts).

JSON:
{{
  "adjusted_score": 85.2,
  "justification": "Time regressed 12%, but mem improved"
}}
    """,

    "test_generator": """
Generate pytest perf test for this function diff.

Function: {code}
Baseline: {baseline_time}s

Output pytest code as string:
@pytest.mark.perf
def test_{func_name}():
    ...
    assert result < {baseline} * 1.15
    """,

    "risk_assessment": """
Assess overall PR risk from changed files.

Files: {files}
Perf history: {history}

JSON:
{{
  "overall_risk": "high/medium/low",
  "perf_impact": "Estimate in % slowdown"
}}
    """
}

def get_prompt(name: str, **kwargs) -> str:
    return PROMPTS[name].format(**kwargs)

