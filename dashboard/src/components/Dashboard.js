import React from 'react';
import ScoreCard from './ScoreCard';
import MetricsCard from './MetricsCard';
import AIAnalysisCard from './AIAnalysisCard';
import RecommendationsCard from './RecommendationsCard';

const Dashboard = ({ data }) => {
  if (!data) return null;

  return (
    <div className="dashboard-grid">
      <ScoreCard
        score={data.performance_score}
        verdict={data.verdict}
        blockMerge={data.block_merge}
        previousScore={data.previous_score}
        currentScore={data.current_score}
        deltaScore={data.delta_score}
      />

      <MetricsCard
        metrics={data.metrics}
      />

      <AIAnalysisCard
        analysis={data.ai_analysis}
      />

      <RecommendationsCard
        metrics={data.metrics}
        score={data.performance_score}
      />
    </div>
  );
};

export default Dashboard;
