"""
Mega slow function for testing performance regression blocking
"""
import time

def mega_slow_function():
    """Sleeps for 2 seconds - should trigger performance alerts"""
    time.sleep(2.0)
    return "completed"
