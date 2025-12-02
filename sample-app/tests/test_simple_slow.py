"""Simple slow test"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from simple_slow import slow_function

@pytest.mark.perf
def test_slow_function(benchmark):
    """Test slow function"""
    result = benchmark(slow_function)
    assert result == "done"
