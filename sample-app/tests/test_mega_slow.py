  """Test mega slow function"""
  import pytest
  import sys
  from pathlib import Path

  sys.path.insert(0, str(Path(__file__).parent.parent))
  from mega_slow import mega_slow

  @pytest.mark.perf
  def test_mega_slow(benchmark):
      """Test mega slow function"""
      result = benchmark(mega_slow)
      assert result == "very slow"
  EOF
