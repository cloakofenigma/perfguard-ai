const path = require('path');
const fs = require('fs');

module.exports = function(app) {
  // Serve report.json with proper headers
  app.get('/report.json', (req, res) => {
    const reportPath = path.join(__dirname, '..', 'public', 'report.json');

    console.log('[Proxy] Request for /report.json');
    console.log('[Proxy] File path:', reportPath);

    // Check if file exists
    if (!fs.existsSync(reportPath)) {
      console.error('[Proxy] report.json not found!');
      return res.status(404).json({
        error: 'Report not found',
        message: 'Run python3 perfguard/main.py to generate a report'
      });
    }

    // Read and serve the file with proper headers
    try {
      const data = fs.readFileSync(reportPath, 'utf8');
      const stats = fs.statSync(reportPath);

      console.log('[Proxy] File found, size:', stats.size, 'bytes');
      console.log('[Proxy] Last modified:', stats.mtime);

      res.setHeader('Content-Type', 'application/json');
      res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
      res.setHeader('Pragma', 'no-cache');
      res.setHeader('Expires', '0');

      // Parse and log scores for debugging
      try {
        const parsed = JSON.parse(data);
        console.log('[Proxy] Serving scores:', {
          previous: parsed.previous_score,
          current: parsed.current_score,
          delta: parsed.delta_score
        });
      } catch (e) {
        console.warn('[Proxy] Could not parse JSON:', e.message);
      }

      res.send(data);
    } catch (error) {
      console.error('[Proxy] Error reading file:', error);
      res.status(500).json({
        error: 'Failed to read report',
        message: error.message
      });
    }
  });
};
