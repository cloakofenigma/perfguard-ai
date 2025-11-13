PROMPTS = {
    "diff_analysis": """
You are a performance engineer. Analyze this git diff for perf risks.

Diff: {diff}

Rules:
- Identify hotspots (loops, I/O, allocations)
- Suggest 3-5 pytest benchmarks
- Risk 0-1 (1=high)

JSON output only:
{{
  "risk_score": 0.78,
  "critical_paths": ["src/payment.py"],
  "suggested_benchmarks": ["test_process_batch", "test_image_resize"],
  "reasoning": "N+1 queries detected",
  "suggestions": ["Add indexing to DB queries"]
}}
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

