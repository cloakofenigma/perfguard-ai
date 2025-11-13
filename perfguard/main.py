#!/usr/bin/env python3
import os
import json
import subprocess
from ai_analyzer import analyze_diff_with_claude
from metrics_collector import collect_metrics
from rules_engine import calculate_score

def main():
    # Step 1: Get git diff
    diff = subprocess.check_output(['git', 'diff', 'HEAD~1']).decode('utf-8')
    
    # Step 2: AI Analysis
    ai_response = analyze_diff_with_claude(diff)
    
    # Step 3: Run selected tests & collect metrics
    metrics = collect_metrics(ai_response['suggested_benchmarks'])
    
    # Step 4: Calculate score
    score_data = calculate_score(metrics, ai_response)
    
    # Output
    with open('perfguard_score.json', 'w') as f:
        json.dump(score_data, f)
    
    # Generate Markdown report
    report = f"""
## PerfGuard AI Report

**Score: {score_data['performance_score']:.1f} / 100**  
**Verdict: {'✅ PASS' if score_data['block_merge'] == False else '🚫 BLOCKED'}**

### Key Metrics
{json.dumps(score_data['metrics'], indent=2)}

### AI Insights
{ai_response['reasoning']}

### Fix Suggestions
{ai_response['suggestions']}
    """
    with open('perfguard_report.md', 'w') as f:
        f.write(report.strip())

if __name__ == '__main__':
    main()

