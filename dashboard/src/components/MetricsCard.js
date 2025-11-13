import React from 'react';

const MetricsCard = ({ metrics }) => {
  if (!metrics) return null;

  const getScoreClass = (score) => {
    if (score >= 90) return 'score-excellent';
    if (score >= 80) return 'score-good';
    if (score >= 70) return 'score-warning';
    return 'score-poor';
  };

  const formatMetricName = (name) => {
    return name
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const getMetricIcon = (name) => {
    const icons = {
      execution_time: '⏱️',
      memory_rss: '💾',
      cpu_utilization: '🖥️',
      io_latency: '📁',
      complexity: '🔢',
      ai_risk: '🤖'
    };
    return icons[name] || '📊';
  };

  const formatValue = (name, value) => {
    if (name === 'execution_time') return `${value.toFixed(4)}s`;
    if (name === 'memory_rss') return `${value.toFixed(2)} MB`;
    if (name === 'cpu_utilization') return `${value.toFixed(2)}%`;
    if (name === 'io_latency') return `${value.toFixed(4)}ms`;
    if (name === 'complexity') return Math.round(value);
    if (name === 'ai_risk') return value.toFixed(2);
    return value;
  };

  const renderMetricItem = ([name, metricData]) => {
    const score = metricData.score || 0;
    const current = metricData.current !== undefined ? metricData.current : metricData.risk_score;
    const baseline = metricData.baseline;
    const change = metricData.change;

    return (
      <li key={name} className="metric-item">
        <div className="metric-header">
          <div className="metric-name">
            <span>{getMetricIcon(name)}</span>
            <span>{formatMetricName(name)}</span>
          </div>
          <div className={`metric-score ${getScoreClass(score)}`}>
            {score.toFixed(0)}
          </div>
        </div>

        <div className="metric-bar">
          <div
            className="metric-bar-fill"
            style={{ width: `${Math.min(score, 100)}%` }}
          />
        </div>

        <div className="metric-details">
          {current !== undefined && (
            <div className="metric-detail">
              <span className="metric-detail-label">Current</span>
              <span className="metric-detail-value">{formatValue(name, current)}</span>
            </div>
          )}
          {baseline !== undefined && (
            <div className="metric-detail">
              <span className="metric-detail-label">Baseline</span>
              <span className="metric-detail-value">{formatValue(name, baseline)}</span>
            </div>
          )}
          {change !== undefined && (
            <div className="metric-detail">
              <span className="metric-detail-label">Change</span>
              <span className={`metric-detail-value ${change < 0 ? 'score-excellent' : change > 10 ? 'score-poor' : ''}`}>
                {change > 0 ? '+' : ''}{change.toFixed(2)}%
              </span>
            </div>
          )}
        </div>
      </li>
    );
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Performance Metrics</h2>
        <div className="card-icon">📈</div>
      </div>

      <ul className="metrics-list">
        {Object.entries(metrics).map(renderMetricItem)}
      </ul>
    </div>
  );
};

export default MetricsCard;
