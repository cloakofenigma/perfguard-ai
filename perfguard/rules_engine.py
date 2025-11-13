import json

def calculate_score(metrics: dict, ai_response: dict) -> dict:
    # Weighted formula
    time_score = min(100, max(0, 100 - (metrics.get('exec_time', 0) * 10)))  # Example
    # ... similar for others
    
    raw_score = (30 * time_score + 20 * mem_score + 15 * cpu_score + 10 * (1 - ai_response['risk_score']) * 100)
    
    # GenAI refine (call Claude again if needed)
    final_score = raw_score  # Simplified
    
    block = final_score < 80
    
    return {
        'performance_score': final_score,
        'block_merge': block,
        'metrics': metrics
    }

