"""
Sample Movie Application - IMDB-like Interface
Modern, responsive Flask application for PerfGuard AI testing
"""
from flask import Flask, render_template, jsonify, request
import json
from movies_data import get_all_movies, get_movie_by_id, search_movies, get_top_rated_movies
from slow_function import (
    process_movie_data_slow,
    calculate_recommendations_slow,
    fetch_user_ratings_slow
)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    """Home page showing top 15 movies"""
    movies = get_all_movies()
    return render_template('index.html', movies=movies)


@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """Movie detail page"""
    movie = get_movie_by_id(movie_id)
    if movie:
        return render_template('movie_detail.html', movie=movie)
    else:
        return "Movie not found", 404


@app.route('/api/movies')
def api_movies():
    """API endpoint to get all movies"""
    movies = get_all_movies()
    return jsonify(movies)


@app.route('/api/movie/<int:movie_id>')
def api_movie(movie_id):
    """API endpoint to get single movie"""
    movie = get_movie_by_id(movie_id)
    if movie:
        return jsonify(movie)
    else:
        return jsonify({"error": "Movie not found"}), 404


@app.route('/api/search')
def api_search():
    """API endpoint to search movies"""
    query = request.args.get('q', '')
    if query:
        results = search_movies(query)
        return jsonify(results)
    return jsonify([])


@app.route('/api/top-rated')
def api_top_rated():
    """API endpoint for top rated movies"""
    limit = request.args.get('limit', 10, type=int)
    movies = get_top_rated_movies(limit)
    return jsonify(movies)


@app.route('/api/recommendations/<int:movie_id>')
def api_recommendations(movie_id):
    """
    API endpoint for movie recommendations
    This endpoint intentionally uses slow function for performance testing
    """
    movie = get_movie_by_id(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    # Intentionally slow function for performance testing
    recommendations = calculate_recommendations_slow(movie)
    return jsonify(recommendations)


@app.route('/api/user-ratings/<int:user_id>')
def api_user_ratings(user_id):
    """
    API endpoint for user ratings
    Uses slow function to simulate database queries
    """
    ratings = fetch_user_ratings_slow(user_id)
    return jsonify(ratings)


@app.route('/api/process-batch', methods=['POST'])
def api_process_batch():
    """
    Process multiple movies (batch operation)
    Intentionally slow for testing
    """
    data = request.get_json()
    movie_ids = data.get('movie_ids', [])

    results = []
    for movie_id in movie_ids:
        movie = get_movie_by_id(movie_id)
        if movie:
            processed = process_movie_data_slow(movie)
            results.append(processed)

    return jsonify(results)


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "movie-app"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

  @app.route("/api/slow-search")
  def slow_search():
      """Intentionally slow search for demo"""
      movies = []
      for i in range(1000):  # O(n²) complexity
          for movie in MOVIES_DATA:
              if movie["title"]:
                  movies.append(movie)
      return jsonify(movies[:10])
  
