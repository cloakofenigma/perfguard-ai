import React from 'react';

const ScoreCard = ({ score, verdict }) => {
  const getVerdictClass = (verdict) => {
    if (!verdict) return 'verdict-pass';
    const v = verdict.toUpperCase();
    if (v === 'EXCELLENT' || v === 'APPROVED') return 'verdict-excellent';
    if (v === 'PASS') return 'verdict-pass';
    if (v === 'WARNING') return 'verdict-warning';
    return 'verdict-fail';
  };

  const getScoreColor = (score) => {
    if (score >= 90) return '#10b981'; // success
    if (score >= 80) return '#6366f1'; // primary
    if (score >= 70) return '#f59e0b'; // warning
    return '#ef4444'; // danger
  };

  return (
    <div className="card score-card">
      <div className="card-header">
        <h2 className="card-title">Performance Score</h2>
        <div className="card-icon">📊</div>
      </div>

      <div className="score-display">
        <div
          className="score-circle"
          style={{ '--score': score }}
        >
          <div className="score-value">{Math.round(score)}</div>
        </div>
      </div>

      <p className="score-label">Overall Performance</p>

      <div className={`verdict-badge ${getVerdictClass(verdict)}`}>
        {verdict || 'PASS'}
      </div>

      <div style={{
        marginTop: '2rem',
        padding: '1rem',
        background: 'var(--bg-tertiary)',
        borderRadius: '0.5rem',
        textAlign: 'left'
      }}>
        <h4 style={{ marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Score Breakdown</h4>
        <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
          <div style={{ marginBottom: '0.25rem' }}>✅ 90-100: Excellent</div>
          <div style={{ marginBottom: '0.25rem' }}>🎯 80-89: Pass</div>
          <div style={{ marginBottom: '0.25rem' }}>⚠️ 70-79: Warning</div>
          <div>❌ 0-69: Fail</div>
        </div>
      </div>
    </div>
  );
};

export default ScoreCard;
