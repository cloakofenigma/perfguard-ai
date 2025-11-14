import React, { useState, useEffect, useCallback } from 'react';
import Dashboard from './components/Dashboard';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const fetchData = useCallback(() => {
    // Add timestamp to prevent caching
    fetch(`${process.env.PUBLIC_URL}/report.json?t=${Date.now()}`)
      .then(res => {
        if (!res.ok) throw new Error('Report not found');
        return res.json();
      })
      .then(reportData => {
        setData(reportData);
        setLoading(false);
        setLastUpdated(new Date());
        setError(null);
      })
      .catch(err => {
        console.error('Error loading report:', err);
        setError(err.message);
        // Set default mock data on error
        setData({
          performance_score: 85,
          verdict: "PASS",
          ai_analysis: {
            risk_score: 0.3,
            reasoning: "No data available. Run PerfGuard AI to generate report."
          },
          metrics: {
            execution_time: { score: 100, current: 0.35, baseline: 0.40, change: -12.5 },
            memory_rss: { score: 95, current: 58.5, baseline: 60.2, change: -2.8 },
            cpu_utilization: { score: 100, current: 0.15, baseline: 0.20, change: -25.0 },
            io_latency: { score: 90, current: 0.35, baseline: 0.30, change: 16.7 },
            complexity: { score: 100, current: 45, baseline: 45, change: 0 },
            ai_risk: { score: 70, risk_score: 0.3 }
          }
        });
        setLoading(false);
        setLastUpdated(new Date());
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
      {error && <div className="error-notice">⚠️ {error}</div>}
      {data && <Dashboard data={data} />}
    </div>
  );
}

export default App;
