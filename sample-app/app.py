"""
Sample Movie Application - IMDB-like Interface
Modern, responsive Flask application for PerfGuard AI testing
"""
from flask import Flask, render_template, jsonify, request
import json
from movies_data import get_all_movies, get_movie_by_id, search_movies, get_top_rated_movies
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


# Slow performance test routes registered from slow_app_new.py


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "movie-app"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
# PerfGuard test - application scope verification
# PerfGuard test - application scope verification
#test comment
