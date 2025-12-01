"""
  Performance regression test - intentionally slow code
  This file tests PerfGuard's ability to detect performance issues
  """
  import time
  import random


  def slow_fibonacci(n):
      """Inefficient recursive fibonacci - O(2^n) complexity"""
      if n <= 1:
          return n
      return slow_fibonacci(n - 1) + slow_fibonacci(n - 2)


  def memory_leak_simulator():
      """Create large data structures that consume memory"""
      large_data = []
      for i in range(100000):
          large_data.append({
              'id': i,
              'data': [random.random() for _ in range(100)],
              'nested': {
                  'values': [j * random.random() for j in range(50)]
              }
          })
      return len(large_data)


  def blocking_operations():
      """Simulate slow I/O with blocking sleeps"""
      results = []
      for i in range(10):
          time.sleep(0.1)  # 100ms per iteration
          results.append(i ** 2)
      return results


  def nested_loops_antipattern(n=500):
      """Nested loops causing O(n^3) complexity"""
      result = 0
      for i in range(n):
          for j in range(n):
              for k in range(100):
                  result += (i * j * k) % 7
      return result


  def inefficient_string_concat():
      """String concatenation in loop - memory inefficient"""
      result = ""
      for i in range(10000):
          result += str(i) + ","  # Creates new string each time
      return result


  def redundant_file_operations():
      """Simulate redundant I/O operations"""
      import tempfile
      import os

      # Create temp file
      temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
      temp_path = temp_file.name

      # Write 1000 times (inefficient)
      for i in range(1000):
          with open(temp_path, 'a') as f:
              f.write(f"Line {i}\n")

      # Read entire file multiple times (redundant)
      content = ""
      for _ in range(100):
          with open(temp_path, 'r') as f:
              content = f.read()

      # Cleanup
      os.unlink(temp_path)
      return len(content)


  class PerformanceRegression:
      """Main class combining all slow operations"""

      def run_slow_operations(self):
          """Execute all slow operations"""
          print("Starting performance regression test...")

          # CPU intensive
          fib_result = slow_fibonacci(25)
          print(f"Fibonacci(25) = {fib_result}")

          # Memory intensive
          mem_result = memory_leak_simulator()
          print(f"Memory test: {mem_result} items created")

          # Blocking I/O
          blocking_result = blocking_operations()
          print(f"Blocking ops: {len(blocking_result)} operations")

          # CPU intensive nested loops
          nested_result = nested_loops_antipattern(300)
          print(f"Nested loops result: {nested_result}")

          # Inefficient string operations
          string_result = inefficient_string_concat()
          print(f"String concat length: {len(string_result)}")

          # File I/O operations
          file_result = redundant_file_operations()
          print(f"File operations: {file_result} bytes")

          return {
              'fibonacci': fib_result,
              'memory': mem_result,
              'blocking': len(blocking_result),
              'nested': nested_result,
              'string': len(string_result),
              'file_io': file_result
          }


  if __name__ == "__main__":
      regression = PerformanceRegression()
      results = regression.run_slow_operations()
      print("\nPerformance Regression Test Complete!")
      print(f"Results: {results}")


