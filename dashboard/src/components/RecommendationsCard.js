import React from 'react';

const RecommendationsCard = ({ metrics, score }) => {
  const generateRecommendations = () => {
    if (!metrics) return [];

    const recommendations = [];

    // Analyze each metric and generate specific recommendations
    Object.entries(metrics).forEach(([metricName, metricData]) => {
      const metricScore = metricData.score || 0;

      if (metricScore < 70) {
        switch (metricName) {
          case 'execution_time':
            recommendations.push({
              metric: 'Execution Time',
              severity: 'high',
              impact: '+30 points',
              fixes: [
                'Profile code with pytest-benchmark to identify slow functions',
                'Optimize nested loops and reduce time complexity',
                'Use caching for repeated calculations',
                'Consider async/await for I/O operations',
                'Replace list comprehensions with generators for large datasets'
              ]
            });
            break;

          case 'memory_rss':
            recommendations.push({
              metric: 'Memory Usage',
              severity: 'high',
              impact: '+20 points',
              fixes: [
                'Use memory_profiler to identify memory leaks',
                'Clear large objects when no longer needed (del statement)',
                'Use generators instead of lists for large data',
                'Avoid global variables holding large datasets',
                'Use __slots__ in classes to reduce memory overhead'
              ]
            });
            break;

          case 'cpu_utilization':
            recommendations.push({
              metric: 'CPU Utilization',
              severity: 'medium',
              impact: '+15 points',
              fixes: [
                'Profile with cProfile to find CPU-intensive operations',
                'Move expensive computations outside loops',
                'Use multiprocessing for CPU-bound tasks',
                'Optimize mathematical operations (use NumPy)',
                'Reduce recursive function calls'
              ]
            });
            break;

          case 'io_latency':
            recommendations.push({
              metric: 'I/O Latency',
              severity: 'medium',
              impact: '+15 points',
              fixes: [
                'Batch file I/O operations instead of multiple small reads/writes',
                'Use connection pooling for database operations',
                'Implement caching for frequently accessed data',
                'Use asynchronous I/O for network operations',
                'Reduce the number of API calls with batching'
              ]
            });
            break;

          case 'complexity':
            recommendations.push({
              metric: 'Code Complexity',
              severity: 'low',
              impact: '+10 points',
              fixes: [
                'Refactor complex functions into smaller, simpler functions',
                'Reduce cyclomatic complexity (max 10 per function)',
                'Extract nested conditions into separate functions',
                'Use early returns to reduce nesting depth',
                'Apply design patterns to simplify logic'
              ]
            });
            break;

          case 'ai_risk':
            recommendations.push({
              metric: 'AI Risk Assessment',
              severity: 'medium',
              impact: '+10 points',
              fixes: [
                'Review and optimize code paths identified by AI analysis',
                'Address performance hotspots mentioned in AI reasoning',
                'Refactor code patterns flagged as risky',
                'Add benchmarks for critical code paths',
                'Document performance-critical sections'
              ]
            });
            break;

          default:
            break;
        }
      } else if (metricScore < 85) {
        // Minor improvements
        const minorFix = {
          metric: metricName.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
          severity: 'low',
          impact: '+5 points',
          fixes: [
            `Minor optimization needed - currently at ${metricScore.toFixed(0)}/100`,
            'Review recent changes for potential improvements',
            'Consider adding more test coverage'
          ]
        };

        // Only add if it's worth mentioning
        if (metricScore < 80) {
          recommendations.push(minorFix);
        }
      }
    });

    // Add general recommendations based on overall score
    if (score < 70) {
      recommendations.push({
        metric: 'Overall Performance',
        severity: 'critical',
        impact: 'Major improvement needed',
        fixes: [
          'Run `pytest -m perf --benchmark-only` to identify bottlenecks',
          'Use profiling tools: cProfile, memory_profiler, line_profiler',
          'Review recent commits for performance regressions',
          'Compare against baseline metrics to see what changed',
          'Consider performance testing in development before committing'
        ]
      });
    }

    return recommendations;
  };

  const recommendations = generateRecommendations();

  if (recommendations.length === 0) {
    return (
      <div className="card recommendations-card">
        <div className="card-header">
          <h2 className="card-title">💡 Recommendations</h2>
          <div className="card-icon">✅</div>
        </div>
        <div className="recommendations-content">
          <div className="all-good">
            <h3>🎉 Excellent Performance!</h3>
            <p>All metrics are performing well. Keep up the good work!</p>
            <div className="tips">
              <h4>Tips to maintain performance:</h4>
              <ul>
                <li>Run performance tests before committing changes</li>
                <li>Monitor metrics after each deployment</li>
                <li>Keep dependencies updated and optimized</li>
                <li>Document performance-critical code sections</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'critical': return 'severity-critical';
      case 'high': return 'severity-high';
      case 'medium': return 'severity-medium';
      case 'low': return 'severity-low';
      default: return '';
    }
  };

  return (
    <div className="card recommendations-card">
      <div className="card-header">
        <h2 className="card-title">💡 How to Improve Score</h2>
        <div className="card-icon">🚀</div>
      </div>

      <div className="recommendations-content">
        <div className="recommendations-summary">
          <p>{recommendations.length} area{recommendations.length > 1 ? 's' : ''} need{recommendations.length === 1 ? 's' : ''} attention</p>
        </div>

        {recommendations.map((rec, index) => (
          <div key={index} className={`recommendation-item ${getSeverityClass(rec.severity)}`}>
            <div className="rec-header">
              <span className="rec-metric">{rec.metric}</span>
              <span className={`rec-severity ${getSeverityClass(rec.severity)}`}>
                {rec.severity.toUpperCase()}
              </span>
              <span className="rec-impact">{rec.impact}</span>
            </div>

            <div className="rec-fixes">
              <h4>Recommended fixes:</h4>
              <ul>
                {rec.fixes.map((fix, fixIndex) => (
                  <li key={fixIndex}>{fix}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}

        <div className="recommendations-footer">
          <h4>🔧 Quick Actions:</h4>
          <div className="quick-actions">
            <code>pytest -m perf -v</code> - Run performance tests
            <code>python -m cProfile perfguard/main.py</code> - Profile code
            <code>memory_profiler your_script.py</code> - Check memory usage
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecommendationsCard;
