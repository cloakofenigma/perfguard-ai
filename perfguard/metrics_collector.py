import pytest
import subprocess
from memory_profiler import profile
import psutil
import time

def collect_metrics(benchmarks: list) -> dict:
    metrics = {}
    for bench in benchmarks:
        # Run benchmark (example: pytest)
        start_time = time.time()
        result = subprocess.run(['pytest', '-m', 'perf', '--benchmark-only'], capture_output=True)
        exec_time = time.time() - start_time
        
        # Memory profiling
        @profile
        def dummy_func(): pass  # Replace with actual
        
        # CPU via psutil
        cpu = psutil.cpu_percent()
        
        metrics[bench] = {
            'exec_time': exec_time,
            'memory_peak': 0,  # From profiler
            'cpu_util': cpu
        }
    return metrics

