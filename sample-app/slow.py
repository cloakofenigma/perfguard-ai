def waste_time():
	total=o
	for i in range(100_000_000):
		total+=i
	return total
	
	  @app.route("/api/slow-search")
  def slow_search():
      """Intentionally slow search for demo"""
      movies = []
      for i in range(1000):  # O(n²) complexity
          for movie in MOVIES_DATA:
              if movie["title"]:
                  movies.append(movie)
      return jsonify(movies[:10])

