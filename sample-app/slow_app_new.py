  """
  Intentionally slow page for testing PerfGuard AI
  Contains multiple performance issues to demonstrate score reduction
  """

  import time
  import random
  from flask import render_template, request

  def create_unoptimized_data():
      """Generate large dataset with inefficient processing"""
      data = []
      # Inefficient nested loops - O(n²) complexity
      for i in range(500):
          for j in range(500):
              if i * j % 7 == 0:
                  data.append({
                      'id': i * j,
                      'value': random.random(),
                      'timestamp': time.time()
                  })
      return data

  def slow_image_processing(image_count=50):
      """Simulate slow image processing without optimization"""
      images = []
      for i in range(image_count):
          # Simulate loading unoptimized large images
          time.sleep(0.01)  # Each image takes 10ms to "load"
          images.append({
              'url': f'/static/images/unoptimized_image_{i}.jpg',
              'size': random.randint(5000, 15000),  # KB - very large!
              'width': 4000,  # High resolution
              'height': 3000,
              'format': 'jpg',
              'compressed': False
          })
      return images

  def inefficient_filtering(items, filter_value):
      """Inefficient filtering with multiple passes"""
      # Pass 1: Filter
      filtered = []
      for item in items:
          if item['value'] > filter_value:
              filtered.append(item)

      # Pass 2: Sort (bubble sort - O(n²))
      n = len(filtered)
      for i in range(n):
          for j in range(0, n-i-1):
              if filtered[j]['value'] > filtered[j+1]['value']:
                  filtered[j], filtered[j+1] = filtered[j+1], filtered[j]

      # Pass 3: Transform
      result = []
      for item in filtered:
          result.append({
              'id': item['id'],
              'computed': item['value'] ** 2,
              'string': str(item['value']) * 100  # Large string
          })

      return result

  def memory_intensive_operation():
      """Create memory-intensive structures"""
      large_lists = []
      for i in range(100):
          # Create 100 large lists
          large_lists.append([random.random() for _ in range(10000)])

      # Don't release memory
      return large_lists

  def blocking_io_simulation():
      """Simulate blocking I/O operations"""
      results = []
      for i in range(20):
          # Simulate slow database query
          time.sleep(0.05)  # 50ms per query
          results.append({
              'query_id': i,
              'data': [random.random() for _ in range(1000)]
          })
      return results

  # Route handlers to add to app.py
  def register_slow_routes(app):
      """Add these routes to your Flask app"""

      @app.route('/slow-gallery')
      def slow_gallery():
          """Page with unoptimized images"""
          start_time = time.time()

          # Load unoptimized images
          images = slow_image_processing(50)

          # Inefficient data processing
          data = create_unoptimized_data()
          filtered_data = inefficient_filtering(data, 0.5)

          # Memory intensive operation
          memory_hog = memory_intensive_operation()

          # Blocking I/O
          io_results = blocking_io_simulation()

          processing_time = time.time() - start_time

          return render_template('slow_gallery.html',
              images=images,
              data=filtered_data[:100],  # Limit displayed data
              io_results=io_results,
              processing_time=processing_time
          )

      @app.route('/api/slow-search')
      def slow_search():
          """Intentionally slow search API"""
          query = request.args.get('q', '')

          # Simulate slow processing
          time.sleep(0.5)  # 500ms delay

          # Generate large dataset
          all_data = create_unoptimized_data()

          # Inefficient search - O(n) for each character
          results = []
          for item in all_data:
              item_str = str(item['id']) + str(item['value'])
              if query.lower() in item_str.lower():
                  results.append(item)

          # Inefficient sorting
          for i in range(len(results)):
              for j in range(i + 1, len(results)):
                  if results[i]['value'] > results[j]['value']:
                      results[i], results[j] = results[j], results[i]

          return {
              'query': query,
              'count': len(results),
              'results': results[:50],  # Return first 50
              'processing_time': 0.5
          }

  <!-- sample-app/templates/slow_gallery.html -->
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Slow Gallery - Performance Test</title>
      <style>
          body {
              font-family: Arial, sans-serif;
              margin: 0;
              padding: 20px;
              background: #1a1a1a;
              color: #fff;
          }
          .container {
              max-width: 1200px;
              margin: 0 auto;
          }
          .warning {
              background: #ff6b6b;
              padding: 15px;
              border-radius: 8px;
              margin-bottom: 20px;
          }
          .stats {
              background: #2d2d2d;
              padding: 15px;
              border-radius: 8px;
              margin-bottom: 20px;
          }
          .gallery {
              display: grid;
              grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
              gap: 20px;
              margin-top: 20px;
          }
          .image-card {
              background: #2d2d2d;
              border-radius: 8px;
              padding: 15px;
          }
          .image-placeholder {
              width: 100%;
              height: 200px;
              background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
              border-radius: 4px;
              display: flex;
              align-items: center;
              justify-content: center;
              font-size: 12px;
              color: rgba(255,255,255,0.7);
          }
          .data-table {
              width: 100%;
              border-collapse: collapse;
              margin-top: 20px;
          }
          .data-table th,
          .data-table td {
              padding: 10px;
              text-align: left;
              border-bottom: 1px solid #444;
          }
          .search-box {
              width: 100%;
              padding: 15px;
              font-size: 16px;
              border: 2px solid #667eea;
              border-radius: 8px;
              background: #2d2d2d;
              color: #fff;
              margin-bottom: 20px;
          }
          .loading {
              text-align: center;
              padding: 40px;
              font-size: 18px;
              color: #667eea;
          }
      </style>
  </head>
  <body>
      <div class="container">
          <h1>🐌 Slow Gallery - Performance Test Page</h1>

          <div class="warning">
              ⚠️ <strong>Warning:</strong> This page is intentionally slow for testing PerfGuard AI.
              It contains multiple performance issues including unoptimized images,
              inefficient loops, and blocking I/O operations.
          </div>

          <div class="stats">
              <h3>Performance Issues:</h3>
              <ul>
                  <li>✗ {{ images|length }} unoptimized images (4000x3000px, uncompressed)</li>
                  <li>✗ O(n²) nested loops processing {{ data|length }} items</li>
                  <li>✗ Blocking I/O operations: {{ io_results|length }} queries</li>
                  <li>✗ Memory-intensive data structures</li>
                  <li>✗ Inefficient bubble sort algorithm</li>
                  <li>✗ Server processing time: {{ "%.2f"|format(processing_time) }}s</li>
              </ul>
          </div>

          <!-- Slow Search -->
          <h2>🔍 Search (Intentionally Slow)</h2>
          <input type="text" 
                 class="search-box" 
                 id="searchBox" 
                 placeholder="Type to search (will take 500ms per query)...">
          <div id="searchResults" class="loading"></div>

          <!-- Unoptimized Image Gallery -->
          <h2>🖼️ Unoptimized Image Gallery</h2>
          <div class="gallery">
              {% for image in images %}
              <div class="image-card">
                  <div class="image-placeholder">
                      {{ image.width }}x{{ image.height }}px<br>
                      {{ image.size }}KB<br>
                      Uncompressed {{ image.format.upper() }}
                  </div>
                  <p style="font-size: 12px; margin-top: 10px; color: #999;">
                      Image {{ loop.index }} - Not optimized, not lazy-loaded
                  </p>
              </div>
              {% endfor %}
          </div>

          <!-- Inefficiently Processed Data -->
          <h2>📊 Inefficiently Processed Data</h2>
          <table class="data-table">
              <thead>
                  <tr>
                      <th>ID</th>
                      <th>Computed Value</th>
                      <th>Large String (truncated)</th>
                  </tr>
              </thead>
              <tbody>
                  {% for item in data[:20] %}
                  <tr>
                      <td>{{ item.id }}</td>
                      <td>{{ "%.4f"|format(item.computed) }}</td>
                      <td>{{ item.string[:50] }}...</td>
                  </tr>
                  {% endfor %}
              </tbody>
          </table>

          <!-- I/O Results -->
          <h2>💾 Blocking I/O Results</h2>
          <div class="stats">
              <p>Executed {{ io_results|length }} blocking queries (50ms each)</p>
              <p>Total I/O time: {{ io_results|length * 50 }}ms</p>
          </div>

      </div>

      <script>
          // Inefficient search implementation
          let searchTimeout;
          document.getElementById('searchBox').addEventListener('input', function(e) {
              clearTimeout(searchTimeout);
              const query = e.target.value;

              if (query.length < 2) {
                  document.getElementById('searchResults').innerHTML = '';
                  return;
              }

              document.getElementById('searchResults').innerHTML =
                  '<div class="loading">Searching... (this will take 500ms)</div>';

              searchTimeout = setTimeout(() => {
                  fetch(`/api/slow-search?q=${encodeURIComponent(query)}`)
                      .then(r => r.json())
                      .then(data => {
                          document.getElementById('searchResults').innerHTML = `
                              <div class="stats">
                                  <strong>Found ${data.count} results</strong> in ${data.processing_time * 1000}ms
                                  <p>First ${data.results.length} results shown</p>
                              </div>
                          `;
                      });
              }, 100);
          });

          // Simulate heavy client-side processing
          setInterval(() => {
              // Inefficient DOM manipulation
              const cards = document.querySelectorAll('.image-card');
              cards.forEach(card => {
                  // Force reflow
                  card.style.transform = `scale(${1 + Math.random() * 0.01})`;
              });
          }, 1000);
      </script>
  </body>
  </html>


