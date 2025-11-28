import React from 'react';

const ScoreCard = ({ score, verdict, blockMerge, previousScore, currentScore, deltaScore }) => {
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

  const getTrendIcon = (current, previous) => {
    const diff = current - previous;
    if (diff > 2) return '📈';
    if (diff < -2) return '📉';
    return '➡️';
  };

  const getTrendText = (current, previous) => {
    const diff = current - previous;
    if (diff > 0) return `+${diff.toFixed(1)}`;
    if (diff < 0) return diff.toFixed(1);
    return '0.0';
  };

  // Use provided scores or fallback to legacy score
  const prev = previousScore !== undefined ? previousScore : score;
  const curr = currentScore !== undefined ? currentScore : score;
  const delta = deltaScore !== undefined ? deltaScore : score;

  return (
    <div className="card score-card">
      <div className="card-header">
        <h2 className="card-title">Performance Scores</h2>
        <div className="card-icon">📊</div>
      </div>

      {/* Info Banner */}
      <div style={{
        padding: '0.75rem 1rem',
        background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(16, 185, 129, 0.1))',
        borderRadius: '0.5rem',
        marginBottom: '1.5rem',
        border: '1px solid rgba(99, 102, 241, 0.2)'
      }}>
        <p style={{
          fontSize: '0.875rem',
          color: 'var(--text-secondary)',
          margin: 0,
          lineHeight: '1.5'
        }}>
          <strong>How to read:</strong> Compare <strong>Baseline</strong> (before) with <strong>Overall</strong> (after) to see the performance impact of your changes.
        </p>
      </div>

      {/* Two Score Display */}
      <div className="two-score-container" style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        gap: '3rem',
        marginBottom: '2rem'
      }}>
        {/* Previous Score */}
        <div className="score-item">
          <div className="score-mini-circle" style={{
            borderColor: getScoreColor(prev),
            width: '120px',
            height: '120px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderWidth: '3px',
            borderStyle: 'solid',
            borderRadius: '50%'
          }}>
            <div className="score-mini-value" style={{
              color: getScoreColor(prev),
              fontSize: '2.5rem',
              fontWeight: 'bold'
            }}>
              {Math.round(prev)}
            </div>
          </div>
          <p className="score-mini-label" style={{
            marginTop: '0.75rem',
            fontWeight: '600',
            fontSize: '1rem'
          }}>Baseline Score</p>
          <p className="score-mini-desc">App before this commit</p>
        </div>

        {/* Arrow/Trend Indicator */}
        <div style={{
          fontSize: '3rem',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
          <span>{getTrendIcon(curr, prev)}</span>
          <span style={{
            fontSize: '1rem',
            fontWeight: '600',
            color: curr >= prev ? '#10b981' : '#ef4444'
          }}>
            {getTrendText(curr, prev)}
          </span>
        </div>

        {/* Current Score */}
        <div className="score-item">
          <div className="score-circle" style={{
            '--score': curr,
            width: '140px',
            height: '140px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: `4px solid ${getScoreColor(curr)}`,
            borderRadius: '50%',
            background: `radial-gradient(circle, rgba(99, 102, 241, 0.1), transparent)`
          }}>
            <div className="score-value" style={{
              fontSize: '3rem',
              fontWeight: 'bold',
              color: getScoreColor(curr)
            }}>{Math.round(curr)}</div>
          </div>
          <p className="score-label" style={{
            marginTop: '0.75rem',
            fontWeight: '600',
            fontSize: '1.1rem'
          }}>Overall Score</p>
          <p className="score-mini-desc">App with this commit</p>
        </div>
      </div>

      {/* Verdict and Merge Status */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '1rem',
        marginTop: '1.5rem',
        marginBottom: '1.5rem'
      }}>
        {/* Verdict */}
        <div style={{
          padding: '1.25rem',
          background: verdict?.toUpperCase() === 'PASS' || verdict?.toUpperCase() === 'EXCELLENT'
            ? 'linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05))'
            : verdict?.toUpperCase() === 'WARNING'
            ? 'linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05))'
            : 'linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05))',
          borderRadius: '0.75rem',
          border: verdict?.toUpperCase() === 'PASS' || verdict?.toUpperCase() === 'EXCELLENT'
            ? '2px solid rgba(16, 185, 129, 0.3)'
            : verdict?.toUpperCase() === 'WARNING'
            ? '2px solid rgba(245, 158, 11, 0.3)'
            : '2px solid rgba(239, 68, 68, 0.3)',
          textAlign: 'center'
        }}>
          <div style={{
            fontSize: '0.75rem',
            color: 'var(--text-muted)',
            marginBottom: '0.5rem',
            textTransform: 'uppercase',
            letterSpacing: '0.5px'
          }}>
            Verdict
          </div>
          <div style={{
            fontSize: '1.5rem',
            fontWeight: 'bold',
            color: verdict?.toUpperCase() === 'PASS' || verdict?.toUpperCase() === 'EXCELLENT'
              ? '#10b981'
              : verdict?.toUpperCase() === 'WARNING'
              ? '#f59e0b'
              : '#ef4444'
          }}>
            {verdict?.toUpperCase() === 'EXCELLENT' ? '✨ EXCELLENT' :
             verdict?.toUpperCase() === 'PASS' ? '✅ PASS' :
             verdict?.toUpperCase() === 'WARNING' ? '⚠️ WARNING' :
             '❌ FAIL'}
          </div>
        </div>

        {/* Merge Status */}
        <div style={{
          padding: '1.25rem',
          background: blockMerge
            ? 'linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05))'
            : 'linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05))',
          borderRadius: '0.75rem',
          border: blockMerge
            ? '2px solid rgba(239, 68, 68, 0.3)'
            : '2px solid rgba(16, 185, 129, 0.3)',
          textAlign: 'center'
        }}>
          <div style={{
            fontSize: '0.75rem',
            color: 'var(--text-muted)',
            marginBottom: '0.5rem',
            textTransform: 'uppercase',
            letterSpacing: '0.5px'
          }}>
            Merge Status
          </div>
          <div style={{
            fontSize: '1.5rem',
            fontWeight: 'bold',
            color: blockMerge ? '#ef4444' : '#10b981'
          }}>
            {blockMerge ? '🚫 BLOCKED' : '✅ APPROVED'}
          </div>
          <div style={{
            fontSize: '0.75rem',
            color: 'var(--text-muted)',
            marginTop: '0.5rem'
          }}>
            {blockMerge ? 'Fix issues before merge' : 'Safe to merge'}
          </div>
        </div>
      </div>

      <div style={{
        marginTop: '1rem',
        padding: '1rem',
        background: 'var(--bg-tertiary)',
        borderRadius: '0.5rem',
        textAlign: 'left'
      }}>
        <h4 style={{ marginBottom: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Score Guide</h4>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          <div style={{ marginBottom: '0.25rem' }}>✨ 90-100: Excellent</div>
          <div style={{ marginBottom: '0.25rem' }}>✅ 80-89: Pass</div>
          <div style={{ marginBottom: '0.25rem' }}>⚠️ 70-79: Warning</div>
          <div>❌ 0-69: Fail (Merge Blocked)</div>
        </div>
      </div>
    </div>
  );
};

export default ScoreCard;
