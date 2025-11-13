"""
Slow Functions for Performance Testing
These functions intentionally have performance issues to test PerfGuard AI
"""
import time
import random
from typing import List, Dict, Any


def process_movie_data_slow(movie: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process movie data with intentional performance issues
    - Unnecessary nested loops
    - Inefficient string operations
    - Memory wastage
    """
    # Intentional delay
    time.sleep(0.5)

    # Inefficient string concatenation
    description = ""
    for _ in range(1000):
        description += "Movie: " + movie["title"] + " "

    # Unnecessary nested loops
    data = []
    for i in range(100):
        for j in range(100):
            data.append(i * j)

    # Memory-intensive operation
    large_list = [movie.copy() for _ in range(10000)]

    return {
        "title": movie["title"],
        "processed": True,
        "data_size": len(data),
        "description_length": len(description)
    }


def calculate_recommendations_slow(movie: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Calculate movie recommendations with N+1 query pattern
    Simulates inefficient database queries
    """
    recommendations = []

    # Simulate N+1 queries (very inefficient)
    for i in range(50):
        # Simulate database query delay
        time.sleep(0.1)

        # Inefficient data processing
        score = 0
        for genre in movie["genre"]:
            for char in genre:
                score += ord(char)

        recommendations.append({
            "movie_id": i,
            "score": score % 100,
            "reason": "Similar to " + movie["title"]
        })

    return recommendations


def fetch_user_ratings_slow(user_id: int) -> Dict[str, Any]:
    """
    Fetch user ratings with poor database query patterns
    """
    # Simulate slow database connection
    time.sleep(1.0)

    # Inefficient data structure
    all_ratings = {}
    for i in range(1000):
        all_ratings[f"movie_{i}"] = random.randint(1, 10)

    # Unnecessary sorting and filtering
    sorted_ratings = dict(sorted(all_ratings.items(), key=lambda x: x[1], reverse=True))

    # Memory-intensive operation
    user_data = {
        "user_id": user_id,
        "ratings": sorted_ratings,
        "history": [sorted_ratings.copy() for _ in range(100)]
    }

    return user_data


def search_movies_inefficient(query: str, all_movies: List[Dict]) -> List[Dict]:
    """
    Inefficient search implementation
    - Linear search instead of indexing
    - Case-insensitive comparison done repeatedly
    """
    results = []

    # Inefficient: converting to lowercase repeatedly
    for movie in all_movies:
        if query.lower() in movie["title"].lower():
            # Unnecessary deep copy
            movie_copy = movie.copy()
            for key in movie:
                movie_copy[key] = movie[key]
            results.append(movie_copy)

    # Unnecessary sorting
    results.sort(key=lambda x: x["title"])
    results.sort(key=lambda x: x["rating"], reverse=True)
    results.sort(key=lambda x: len(x["title"]))

    return results


def load_movie_details_n_plus_one(movie_ids: List[int]) -> List[Dict]:
    """
    Classic N+1 query problem
    """
    movies = []

    for movie_id in movie_ids:
        # Simulate individual database query for each movie
        time.sleep(0.05)

        # Simulate fetching movie details
        movie = {"id": movie_id, "title": f"Movie {movie_id}"}

        # Simulate fetching cast (another query)
        time.sleep(0.05)
        movie["cast"] = [f"Actor {i}" for i in range(5)]

        # Simulate fetching crew (another query)
        time.sleep(0.05)
        movie["crew"] = {"director": f"Director {movie_id}"}

        movies.append(movie)

    return movies


def process_large_dataset():
    """
    Process large dataset inefficiently
    - No streaming
    - Loads everything in memory
    """
    # Simulate loading large dataset
    data = []
    for i in range(100000):
        data.append({
            "id": i,
            "value": random.random(),
            "metadata": {"key": f"value_{i}"}
        })

    # Inefficient filtering
    filtered = [item for item in data if item["value"] > 0.5]

    # Inefficient aggregation
    total = sum([item["value"] for item in filtered])

    return len(filtered), total


def complex_nested_loops(n: int = 100):
    """
    Unnecessary complex nested loops
    O(n^3) complexity when O(n) would suffice
    """
    result = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result += i + j + k

    return result


def inefficient_string_building(iterations: int = 10000):
    """
    Inefficient string concatenation
    Should use join() instead
    """
    result = ""
    for i in range(iterations):
        result += f"Item {i}, "

    return result


def memory_leak_simulation():
    """
    Simulates memory leak by holding references unnecessarily
    """
    cached_data = []

    for i in range(10000):
        large_object = {
            "id": i,
            "data": [random.random() for _ in range(1000)],
            "metadata": {"timestamp": time.time()}
        }
        cached_data.append(large_object)

    # Never cleared!
    return len(cached_data)
