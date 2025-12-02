"""
JUNK CODE - Intentionally terrible performance
This code is designed to fail PerfGuard checks and BLOCK merges
Expected: Score < 80, Verdict: FAIL, Merge: BLOCKED
"""
import time
import random
import json
import tempfile
import os


def recursive_fibonacci_nightmare(n):
    """
    Pure recursive fibonacci - O(2^n) exponential complexity
    Will cause massive CPU spike and execution time explosion
    """
    if n <= 1:
        return n
    return recursive_fibonacci_nightmare(n - 1) + recursive_fibonacci_nightmare(n - 2)


def memory_bomb():
    """
    Create massive memory allocation - 100MB+ of wasted memory
    Simulates memory leak and inefficient data structures
    """
    garbage = []
    for i in range(500000):  # Half a million objects
        garbage.append({
            'id': i,
            'wasted_space': [random.random() for _ in range(200)],  # 200 floats per object
            'more_waste': {
                'nested': [j * random.random() for j in range(100)],
                'duplicate_data': str(i) * 50,  # Repeat string 50 times
                'pointless_list': list(range(100))
            }
        })
    return len(garbage)


def blocking_io_nightmare():
    """
    Simulate extremely slow I/O with blocking operations
    Will cause I/O latency to skyrocket
    """
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    temp_path = temp_file.name

    # Write operation - extremely slow
    for i in range(2000):
        with open(temp_path, 'a') as f:
            time.sleep(0.001)  # 1ms per write = 2 seconds total
            f.write(f"Junk line {i}: " + "x" * 100 + "\n")

    # Read operation - multiple redundant reads
    content = ""
    for _ in range(500):  # Read 500 times
        with open(temp_path, 'r') as f:
            content = f.read()

    # Cleanup
    os.unlink(temp_path)
    return len(content)


def nested_loop_catastrophe(n=300):
    """
    Triple nested loop with O(n^3) complexity
    CPU utilization will go through the roof
    """
    result = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                # Pointless calculations
                result += (i * j * k) % 13
                result += (i + j + k) ** 2
                result -= (i * j) // max(k, 1)
    return result


def string_concatenation_disaster():
    """
    Inefficient string concatenation in loop
    Creates new string object every iteration - terrible for memory
    """
    result = ""
    for i in range(50000):  # 50k iterations
        result += str(i)
        result += ","
        result += str(i * 2)
        result += ";"
    return len(result)


def redundant_json_parsing():
    """
    Parse and re-serialize JSON repeatedly
    Wastes CPU and memory unnecessarily
    """
    data = {
        'items': [{'id': i, 'value': random.random()} for i in range(10000)]
    }

    for _ in range(100):  # 100 redundant operations
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        data = parsed

    return len(data['items'])


def unoptimized_list_operations():
    """
    Terrible list operations - repeatedly copy and filter large lists
    """
    big_list = list(range(100000))

    # Inefficient filtering - creates new list each time
    for _ in range(10):
        big_list = [x for x in big_list if x % 2 == 0]
        big_list = [x for x in big_list if x % 3 == 0]
        big_list = [x for x in big_list if x % 5 == 0]
        big_list = list(range(100000))  # Reset and repeat

    return len(big_list)


def combined_performance_killer():
    """
    Combine ALL performance anti-patterns
    This should DEFINITELY block the merge
    """
    print("🔥 Starting performance killer...")

    # 1. CPU killer - recursive fibonacci
    print("💀 CPU nightmare...")
    fib_result = recursive_fibonacci_nightmare(30)  # Will take several seconds

    # 2. Memory killer
    print("💀 Memory bomb...")
    mem_result = memory_bomb()  # 100MB+ allocation

    # 3. I/O killer
    print("💀 I/O nightmare...")
    io_result = blocking_io_nightmare()  # 2+ seconds of blocking I/O

    # 4. Nested loops
    print("💀 Nested loop catastrophe...")
    loop_result = nested_loop_catastrophe(200)  # 8 million iterations

    # 5. String operations
    print("💀 String concatenation disaster...")
    string_result = string_concatenation_disaster()

    # 6. JSON parsing
    print("💀 Redundant JSON parsing...")
    json_result = redundant_json_parsing()

    # 7. List operations
    print("💀 Unoptimized list operations...")
    list_result = unoptimized_list_operations()

    print("🔥 Performance killer complete!")

    return {
        'fibonacci': fib_result,
        'memory_wasted': mem_result,
        'io_operations': io_result,
        'loop_iterations': loop_result,
        'string_length': string_result,
        'json_items': json_result,
        'list_size': list_result,
        'status': 'This code is terrible and should BLOCK the merge!'
    }


# Flask route to trigger the junk code
def register_junk_routes(app):
    """Register junk performance routes to Flask app"""

    @app.route('/junk/killer')
    def junk_killer():
        """Endpoint that triggers ALL performance anti-patterns"""
        result = combined_performance_killer()
        return app.response_class(
            response=json.dumps(result),
            status=200,
            mimetype='application/json'
        )

    @app.route('/junk/fibonacci')
    def junk_fibonacci():
        """Endpoint for recursive fibonacci"""
        result = recursive_fibonacci_nightmare(28)
        return {'result': result, 'warning': 'O(2^n) complexity!'}

    @app.route('/junk/memory')
    def junk_memory():
        """Endpoint that wastes memory"""
        result = memory_bomb()
        return {'objects_created': result, 'memory_wasted': '~100MB'}

    @app.route('/junk/io')
    def junk_io():
        """Endpoint with blocking I/O"""
        result = blocking_io_nightmare()
        return {'bytes_processed': result, 'warning': 'Extremely slow I/O'}
