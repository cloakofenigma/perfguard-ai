import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const PRScoreChart = ({ data }) => {
  if (!data) return <p>Loading...</p>;

  // Mock trend data (in prod, fetch from API/PRs)
  const trendData = {
    labels: ['PR #1', 'PR #2', 'PR #3', 'PR #4'],
    datasets: [
      {
        label: 'Performance Score',
        data: [92, 76, 85, data.performance_score],
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1,
      },
    ],
  };

  const metricsData = {
    labels: ['Exec Time', 'Memory', 'CPU', 'I/O'],
    datasets: [
      {
        label: 'Current vs Baseline (%)',
        data: [115, 95, 102, 120],  // From data.metrics
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 205, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
        ],
        borderColor: [
          'rgb(255, 99, 132)',
          'rgb(54, 162, 235)',
          'rgb(255, 205, 86)',
          'rgb(75, 192, 192)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: { legend: { position: 'top' }, title: { display: true, text: 'PR Performance Trends' } },
  };

  return (
    <div className="charts">
      <div className="chart">
        <Line options={options} data={trendData} />
      </div>
      <div className="chart">
        <Bar options={options} data={metricsData} />
      </div>
      <div className="suggestions">
        <h3>AI Suggestions</h3>
        <p>{data.suggestions || 'No issues detected!'}</p>
      </div>
    </div>
  );
};

export default PRScoreChart;

