import React, { useState, useEffect, useCallback } from 'react';
import Dashboard from './components/Dashboard';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const fetchData = useCallback(() => {
    console.log('[PerfGuard] Fetching report.json...');

    // Add timestamp to prevent caching
    const url = `/report.json?t=${Date.now()}`;
    console.log('[PerfGuard] Fetch URL:', url);

    fetch(url, {
      cache: 'no-store',
      headers: {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache'
      }
    })
      .then(res => {
        console.log('[PerfGuard] Response status:', res.status);
        console.log('[PerfGuard] Response headers:', res.headers.get('content-type'));

        if (!res.ok) {
          throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }

        // Check if response is JSON
        const contentType = res.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
          throw new Error(`Expected JSON, got ${contentType}`);
        }

        return res.json();
      })
      .then(reportData => {
        console.log('[PerfGuard] Report data loaded:', {
          previous_score: reportData.previous_score,
          current_score: reportData.current_score,
          delta_score: reportData.delta_score,
          performance_score: reportData.performance_score
        });

        // Validate required fields
        if (typeof reportData.performance_score !== 'number') {
          throw new Error('Invalid report data: missing performance_score');
        }

        setData(reportData);
        setLoading(false);
        setLastUpdated(new Date());
        setError(null);
        console.log('[PerfGuard] Dashboard updated successfully!');
      })
      .catch(err => {
        console.error('[PerfGuard] Error loading report:', err);
        console.error('[PerfGuard] Error details:', {
          message: err.message,
          stack: err.stack
        });

        setError(`Failed to load report: ${err.message}`);
        setLoading(false);
        setLastUpdated(new Date());

        // Don't set mock data - show error state instead
        setData(null);
      });
  }, []);

  // Initial load
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Auto-refresh every 30 seconds if enabled
  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(() => {
      fetchData();
    }, 30000); // 30 seconds

    return () => clearInterval(interval);
  }, [autoRefresh, fetchData]);

  if (loading) {
    return (
      <div className="App">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading PerfGuard AI Dashboard...</p>
        </div>
      </div>
    );
  }

  const handleRefresh = () => {
    setLoading(true);
    fetchData();
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🛡️ PerfGuard AI</h1>
        <p>Performance Analysis Dashboard</p>
        <div className="header-controls">
          <button className="refresh-btn" onClick={handleRefresh} disabled={loading}>
            🔄 Refresh
          </button>
          <label className="auto-refresh-toggle">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            <span>Auto-refresh (30s)</span>
          </label>
          {lastUpdated && (
            <span className="last-updated">
              Last updated: {lastUpdated.toLocaleTimeString()}
            </span>
          )}
        </div>
      </header>
      {error && (
        <div className="error-notice" style={{
          padding: '1.5rem',
          margin: '1rem auto',
          maxWidth: '800px',
          background: 'rgba(239, 68, 68, 0.1)',
          border: '2px solid #ef4444',
          borderRadius: '0.5rem',
          color: '#fca5a5'
        }}>
          <h3 style={{marginBottom: '0.5rem'}}>⚠️ Report Load Failed</h3>
          <p style={{marginBottom: '1rem'}}>{error}</p>
          <div style={{fontSize: '0.875rem', color: '#f87171'}}>
            <p><strong>Troubleshooting:</strong></p>
            <ol style={{marginLeft: '1.5rem', marginTop: '0.5rem'}}>
              <li>Run: <code>./venv/bin/python3 perfguard/main.py</code></li>
              <li>Verify: <code>ls -lh dashboard/public/report.json</code></li>
              <li>Check browser console (F12) for detailed errors</li>
              <li>Try hard refresh: Ctrl+Shift+R</li>
            </ol>
          </div>
        </div>
      )}
      {data ? (
        <Dashboard data={data} />
      ) : !loading && !error && (
        <div style={{textAlign: 'center', padding: '3rem', color: 'var(--text-muted)'}}>
          <h2>No Data Available</h2>
          <p>Run PerfGuard AI to generate a performance report.</p>
        </div>
      )}
    </div>
  );
}

export default App;
