import React from 'react';
import ScoreCard from './ScoreCard';
import MetricsCard from './MetricsCard';
import AIAnalysisCard from './AIAnalysisCard';

const Dashboard = ({ data }) => {
  if (!data) return null;

  return (
    <div className="dashboard-grid">
      <ScoreCard
        score={data.performance_score}
        verdict={data.verdict}
      />

      <MetricsCard
        metrics={data.metrics}
      />

      <AIAnalysisCard
        analysis={data.ai_analysis}
      />
    </div>
  );
};

export default Dashboard;
