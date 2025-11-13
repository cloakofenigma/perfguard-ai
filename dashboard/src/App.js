import React, { useState, useEffect } from 'react';
import PRScoreChart from './components/PRScoreChart';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Fetch from /report.json or mock
    fetch('/report.json')
      .then(res => res.json())
      .then(setData);
  }, []);

  return (
    <div className="App">
      <h1>PerfGuard AI Dashboard</h1>
      {data && <PRScoreChart data={data} />}
    </div>
  );
}

export default App;
