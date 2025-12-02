"""
Performance tests for junk code
These tests will cause PerfGuard to BLOCK the merge
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from junk_performance_killer import (
    recursive_fibonacci_nightmare,
    memory_bomb,
    blocking_io_nightmare,
    nested_loop_catastrophe,
    string_concatenation_disaster,
    redundant_json_parsing,
    unoptimized_list_operations,
    combined_performance_killer
)


@pytest.mark.perf
@pytest.mark.junk  # Exclude from normal runs
def test_recursive_fibonacci_slow(benchmark):
    """
    Test recursive fibonacci - will show O(2^n) explosion
    Expected: Execution time >> baseline, FAIL
    """
    result = benchmark(recursive_fibonacci_nightmare, 25)
    assert result >= 0


@pytest.mark.perf
@pytest.mark.junk  # Exclude from normal runs
def test_memory_bomb_benchmark(benchmark):
    """
    Test memory allocation bomb
    Expected: Memory usage >> baseline, FAIL
    """
    result = benchmark(memory_bomb)
    assert result > 0


@pytest.mark.perf
@pytest.mark.junk  # Exclude from normal runs
def test_blocking_io_benchmark(benchmark):
    """
    Test blocking I/O operations
    Expected: I/O latency >> baseline, FAIL
    """
    result = benchmark(blocking_io_nightmare)
    assert result > 0


@pytest.mark.perf
@pytest.mark.junk  # Exclude from normal runs
def test_nested_loops_benchmark(benchmark):
    """
    Test O(n^3) nested loops
    Expected: CPU utilization high, execution time high, FAIL
    """
    result = benchmark(nested_loop_catastrophe, 150)
    assert result >= 0


@pytest.mark.perf
@pytest.mark.junk  # Exclude from normal runs
def test_string_concat_benchmark(benchmark):
    """
    Test inefficient string concatenation
    Expected: Poor memory and CPU performance, FAIL
    """
    result = benchmark(string_concatenation_disaster)
    assert result > 0


@pytest.mark.perf
@pytest.mark.junk  # Exclude from normal runs
def test_json_parsing_benchmark(benchmark):
    """
    Test redundant JSON operations
    Expected: High CPU usage, poor performance, FAIL
    """
    result = benchmark(redundant_json_parsing)
    assert result > 0


@pytest.mark.perf
@pytest.mark.junk  # Exclude from normal runs
def test_list_operations_benchmark(benchmark):
    """
    Test unoptimized list operations
    Expected: Memory and CPU issues, FAIL
    """
    result = benchmark(unoptimized_list_operations)
    assert result > 0


@pytest.mark.perf
@pytest.mark.junk  # Exclude from normal runs
@pytest.mark.slow
def test_combined_killer_benchmark(benchmark):
    """
    Test ALL performance anti-patterns combined
    Expected: CATASTROPHIC performance, GUARANTEED FAIL
    This single test should be enough to BLOCK the merge
    """
    result = benchmark(combined_performance_killer)
    assert 'status' in result
    assert result['fibonacci'] > 0
