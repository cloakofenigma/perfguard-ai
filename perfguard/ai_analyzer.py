import os
import json
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

PROMPT_TEMPLATE = """
You are a senior performance engineer. Analyze this git diff for performance risks.

Diff: {diff}

Output JSON:
{{
  "risk_score": 0.0-1.0,
  "critical_paths": ["file.py"],
  "suggested_benchmarks": ["test_func()"],
  "reasoning": "Explanation",
  "suggestions": ["Fix idea"]
}}
"""

def analyze_diff_with_claude(diff: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(diff=diff)
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    # Parse JSON from response
    content = response.content[0].text
    start = content.find('{')
    end = content.rfind('}') + 1
    json_str = content[start:end]
    return json.loads(json_str)

