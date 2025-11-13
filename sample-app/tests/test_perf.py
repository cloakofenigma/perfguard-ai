"""
Performance Tests for Movie Application
Tests marked with @pytest.mark.perf will be run by PerfGuard AI
"""
import pytest
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app
from movies_data import get_all_movies, get_movie_by_id, search_movies
from slow_function import (
    process_movie_data_slow,
    calculate_recommendations_slow,
    fetch_user_ratings_slow,
    complex_nested_loops
)


@pytest.fixture
def client():
    """Flask test client fixture"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_movie():
    """Sample movie data fixture"""
    return get_movie_by_id(1)


# ============= API Performance Tests =============

@pytest.mark.perf
def test_api_get_all_movies(benchmark, client):
    """Benchmark fetching all movies"""
    result = benchmark(client.get, '/api/movies')
    assert result.status_code == 200
    data = result.get_json()
    assert len(data) == 15


@pytest.mark.perf
def test_api_get_single_movie(benchmark, client):
    """Benchmark fetching single movie"""
    result = benchmark(client.get, '/api/movie/1')
    assert result.status_code == 200
    data = result.get_json()
    assert data['title'] == 'Drishyam'


@pytest.mark.perf
def test_api_search_movies(benchmark, client):
    """Benchmark movie search"""
    def search():
        return client.get('/api/search?q=dark')

    result = benchmark(search)
    assert result.status_code == 200


@pytest.mark.perf
def test_home_page_load(benchmark, client):
    """Benchmark home page loading time"""
    result = benchmark(client.get, '/')
    assert result.status_code == 200
    assert b'CineVault' in result.data


@pytest.mark.perf
def test_movie_detail_page(benchmark, client):
    """Benchmark movie detail page"""
    result = benchmark(client.get, '/movie/1')
    assert result.status_code == 200
    assert b'Drishyam' in result.data


# ============= Database Operation Tests =============

@pytest.mark.perf
def test_get_all_movies_performance(benchmark):
    """Benchmark database query for all movies"""
    result = benchmark(get_all_movies)
    assert len(result) == 15


@pytest.mark.perf
def test_get_movie_by_id_performance(benchmark):
    """Benchmark fetching movie by ID"""
    result = benchmark(get_movie_by_id, 1)
    assert result is not None
    assert result['id'] == 1


@pytest.mark.perf
def test_search_movies_performance(benchmark):
    """Benchmark search functionality"""
    result = benchmark(search_movies, 'knight')
    assert len(result) > 0


# ============= Slow Function Tests (Intentional Performance Issues) =============

@pytest.mark.perf
@pytest.mark.slow
def test_process_movie_data_slow(benchmark, sample_movie):
    """
    Test intentionally slow movie processing
    This should trigger performance warnings
    """
    result = benchmark(process_movie_data_slow, sample_movie)
    assert result['processed'] is True


@pytest.mark.perf
@pytest.mark.slow
def test_calculate_recommendations_slow(benchmark, sample_movie):
    """
    Test slow recommendation calculation
    Should show N+1 query issues
    """
    result = benchmark(calculate_recommendations_slow, sample_movie)
    assert len(result) > 0


@pytest.mark.perf
@pytest.mark.slow
def test_fetch_user_ratings_slow(benchmark):
    """
    Test slow user ratings fetch
    Should show database performance issues
    """
    result = benchmark(fetch_user_ratings_slow, 1)
    assert 'user_id' in result


@pytest.mark.perf
@pytest.mark.slow
def test_complex_nested_loops(benchmark):
    """
    Test O(n^3) complexity algorithm
    Should trigger complexity warnings
    """
    result = benchmark(complex_nested_loops, 50)
    assert result > 0


# ============= Memory Performance Tests =============

@pytest.mark.perf
def test_large_movie_list_memory():
    """Test memory usage when handling large movie lists"""
    movies = get_all_movies()
    # Create multiple copies to test memory
    large_list = [movies.copy() for _ in range(100)]
    assert len(large_list) == 100


@pytest.mark.perf
def test_movie_data_serialization(benchmark):
    """Test JSON serialization performance"""
    import json

    movies = get_all_movies()

    def serialize():
        return json.dumps(movies)

    result = benchmark(serialize)
    assert len(result) > 0


# ============= API Load Tests =============

@pytest.mark.perf
def test_multiple_api_calls(benchmark, client):
    """Simulate multiple API calls"""

    def multiple_calls():
        results = []
        for i in range(1, 6):
            response = client.get(f'/api/movie/{i}')
            results.append(response.get_json())
        return results

    results = benchmark(multiple_calls)
    assert len(results) == 5


@pytest.mark.perf
def test_concurrent_page_loads(benchmark, client):
    """Test concurrent page load performance"""

    def load_pages():
        responses = []
        responses.append(client.get('/'))
        responses.append(client.get('/movie/1'))
        responses.append(client.get('/api/movies'))
        return responses

    results = benchmark(load_pages)
    assert all(r.status_code == 200 for r in results)


# ============= Edge Case Performance Tests =============

@pytest.mark.perf
def test_search_no_results(benchmark, client):
    """Test search performance with no results"""

    def search_empty():
        return client.get('/api/search?q=nonexistentmovie12345')

    result = benchmark(search_empty)
    assert result.status_code == 200
    assert len(result.get_json()) == 0


@pytest.mark.perf
def test_invalid_movie_id(benchmark, client):
    """Test performance with invalid movie ID"""

    def get_invalid():
        return client.get('/api/movie/9999')

    result = benchmark(get_invalid)
    assert result.status_code == 404


# ============= Utility Function Tests =============

def test_movie_data_integrity():
    """Verify movie data structure"""
    movies = get_all_movies()
    for movie in movies:
        assert 'id' in movie
        assert 'title' in movie
        assert 'rating' in movie
        assert 'genre' in movie
        assert 'cast' in movie


@pytest.mark.perf
def test_filtering_top_rated(benchmark):
    """Test filtering performance for top rated movies"""
    from movies_data import get_top_rated_movies

    result = benchmark(get_top_rated_movies, 10)
    assert len(result) == 10
    # Verify sorted by rating
    assert result[0]['rating'] >= result[-1]['rating']


# ============= Configuration =============

def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "perf: Performance test marker for PerfGuard AI"
    )
    config.addinivalue_line(
        "markers", "slow: Tests with intentional performance issues"
    )
