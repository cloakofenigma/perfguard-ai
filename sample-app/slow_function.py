"""
Intentionally slow functions for performance testing
These functions demonstrate common performance anti-patterns
"""
import time
import random


def process_movie_data_slow(movie):
    """
    Simulate slow data processing with unnecessary delays
    Anti-pattern: Blocking I/O in loop
    """
    time.sleep(0.1)  # Simulate slow database query

    # Inefficient data transformation
    result = {}
    for key, value in movie.items():
        time.sleep(0.01)  # Simulate slow processing
        result[key] = value

    result['processed'] = True
    return result


def calculate_recommendations_slow(movie):
    """
    Simulate N+1 query problem
    Anti-pattern: Multiple sequential database calls
    """
    recommendations = []

    # Simulate fetching related movies one by one (N+1 problem)
    for i in range(5):
        time.sleep(0.05)  # Simulate database query
        recommendations.append({
            'id': i,
            'title': f'Related Movie {i}',
            'similarity': random.random()
        })

    return recommendations


def fetch_user_ratings_slow(user_id):
    """
    Simulate slow database query
    Anti-pattern: No connection pooling, no caching
    """
    time.sleep(0.2)  # Simulate slow query

    return {
        'user_id': user_id,
        'ratings': [random.randint(1, 5) for _ in range(10)],
        'average': random.uniform(2.0, 5.0)
    }


def complex_nested_loops(n):
    """
    O(n^3) complexity algorithm
    Anti-pattern: Unnecessary nested loops
    """
    result = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result += (i * j * k) % 7
    return result


def inefficient_string_concat(count=1000):
    """
    String concatenation in loop
    Anti-pattern: Creates new string object each iteration
    """
    result = ""
    for i in range(count):
        result += str(i) + ","
    return result


def memory_intensive_operation():
    """
    Create large data structures
    Anti-pattern: Unnecessary memory allocation
    """
    large_list = []
    for i in range(10000):
        large_list.append({
            'id': i,
            'data': [random.random() for _ in range(100)],
            'nested': {
                'values': [j * random.random() for j in range(50)]
            }
        })
    return len(large_list)
