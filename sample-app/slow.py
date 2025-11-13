from slow_function import process_movie_data_slow, search_movies_inefficient
def waste_time():
	total=o
	for i in range(10_000_000):
		total+=i
	return total
	
	 @app.route('/api/test-slow')
  def test_slow_endpoint():
      """Intentionally slow for performance testing"""
      import time
      # Simulate slow processing
      result = []
      for i in range(100):
          for j in range(100):  # Nested loops - O(n²)
              result.append(i * j)
              time.sleep(0.001)  # Small delay
      return jsonify({"processed": len(result)})

  ---



