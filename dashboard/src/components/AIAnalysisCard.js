import React from 'react';

const AIAnalysisCard = ({ analysis }) => {
  if (!analysis) {
    return (
      <div className="card ai-analysis">
        <div className="card-header">
          <h2 className="card-title">AI Analysis</h2>
          <div className="card-icon">🤖</div>
        </div>
        <div className="ai-content">
          <p style={{ color: 'var(--text-secondary)' }}>
            No AI analysis available. Run PerfGuard AI to generate insights.
          </p>
        </div>
      </div>
    );
  }

  const riskScore = analysis.risk_score !== undefined ? analysis.risk_score : 0.5;
  const reasoning = analysis.reasoning || "No reasoning provided";

  const getRiskLevel = (score) => {
    if (score < 0.3) return { level: 'LOW', class: 'risk-low' };
    if (score < 0.7) return { level: 'MEDIUM', class: 'risk-medium' };
    return { level: 'HIGH', class: 'risk-high' };
  };

  const risk = getRiskLevel(riskScore);

  return (
    <div className="card ai-analysis">
      <div className="card-header">
        <h2 className="card-title">AI Analysis</h2>
        <div className="card-icon">🤖</div>
      </div>

      <div className="ai-content">
        <div className="ai-risk">
          <span style={{ color: 'var(--text-secondary)' }}>Risk Score:</span>
          <span className={`risk-badge ${risk.class}`}>{risk.level}</span>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            ({(riskScore * 100).toFixed(0)}%)
          </span>
        </div>

        <div className="ai-reasoning">
          {reasoning}
        </div>

        {analysis.hotspots && analysis.hotspots.length > 0 && (
          <div style={{ marginTop: '1.5rem' }}>
            <h4 style={{ color: 'var(--text-primary)', marginBottom: '0.75rem' }}>
              🔥 Performance Hotspots
            </h4>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {analysis.hotspots.map((hotspot, index) => (
                <li
                  key={index}
                  style={{
                    padding: '0.75rem',
                    marginBottom: '0.5rem',
                    background: 'var(--bg-dark)',
                    borderRadius: '0.5rem',
                    borderLeft: '3px solid var(--danger-color)'
                  }}
                >
                  <div style={{ fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.25rem' }}>
                    {hotspot.file}:{hotspot.line}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    {hotspot.description}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {analysis.recommendations && analysis.recommendations.length > 0 && (
          <div style={{ marginTop: '1.5rem' }}>
            <h4 style={{ color: 'var(--text-primary)', marginBottom: '0.75rem' }}>
              💡 Recommendations
            </h4>
            <ul style={{ paddingLeft: '1.5rem', color: 'var(--text-secondary)' }}>
              {analysis.recommendations.map((rec, index) => (
                <li key={index} style={{ marginBottom: '0.5rem' }}>
                  {rec}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default AIAnalysisCard;
