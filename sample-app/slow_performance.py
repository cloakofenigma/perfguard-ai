  """
  Performance degradation module for testing PerfGuard.
  This intentionally slows down the app by ~50% for testing purposes.
  """
  import time
  import random

  def inefficient_sort(data):
      """O(n²) bubble sort - intentionally slow"""
      n = len(data)
      for i in range(n):
          for j in range(0, n-i-1):
              if data[j] > data[j+1]:
                  data[j], data[j+1] = data[j+1], data[j]
      return data

  def memory_intensive_operation():
      """Create large data structures to increase memory usage"""
      # Create 10MB of data
      large_list = [random.random() for _ in range(1_000_000)]
      # Perform redundant operations
      result = sum(large_list)
      result = sum(large_list)  # Redundant
      result = sum(large_list)  # Redundant
      return result

  def blocking_io_simulation():
      """Simulate slow I/O operations"""
      time.sleep(0.5)  # Block for 500ms
      return "Slow operation complete"

  def redundant_calculations(n=1000):
      """Perform unnecessary calculations"""
      result = 0
      for i in range(n):
          for j in range(n):
              result += i * j  # O(n²) complexity
      return result

  def unoptimized_data_processing():
      """Process data inefficiently"""
      # Create large unoptimized data
      data = list(range(10000))

      # Inefficient filtering (multiple passes)
      filtered = [x for x in data if x % 2 == 0]
      filtered = [x for x in filtered if x % 3 == 0]
      filtered = [x for x in filtered if x % 5 == 0]

      # Inefficient sorting
      sorted_data = inefficient_sort(filtered[:100])

      return sorted_data

  def slow_route_handler():
      """Combine all slow operations for a route"""
      # This should reduce performance by ~50%
      blocking_io_simulation()
      memory_intensive_operation()
      redundant_calculations(500)
      result = unoptimized_data_processing()

      # Add another blocking operation
      time.sleep(0.3)

      return {
          "message": "This route is intentionally slow for testing",
          "data_size": len(result)
      }
