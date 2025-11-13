import React, { useState, useEffect } from 'react';
import PRScoreChart from './components/PRScoreChart';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Fetch from /report.json with error handling
    fetch('/report.json')
      .then(res => {
        if (!res.ok) throw new Error('Report not found');
        return res.json();
      })
      .then(setData)
      .catch(err => {
        console.error('Error loading report:', err);
        // Set default mock data on error
        setData({
          performance_score: 85,
          verdict: "PASS",
          suggestions: "No data available. Run PerfGuard AI to generate report."
        });
      });
  }, []);

  return (
    <div className="App">
      <h1>PerfGuard AI Dashboard</h1>
      {data && <PRScoreChart data={data} />}
    </div>
  );
}

export default App;
