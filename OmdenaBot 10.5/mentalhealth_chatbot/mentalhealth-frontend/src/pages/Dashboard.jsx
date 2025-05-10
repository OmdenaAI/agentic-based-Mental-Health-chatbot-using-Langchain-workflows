import { useEffect, useState } from 'react';
import axios from 'axios';
import { Line, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  LineElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/dashboard-data')
      .then(res => setData(res.data))
      .catch(() => alert('Error loading dashboard data'));
  }, []);

  if (!data) return <p style={{ padding: '2rem' }}>Loading dashboard...</p>;

  const moodData = {
    labels: Object.keys(data.mood_by_date),
    datasets: [{
      label: 'Mood Score',
      data: Object.values(data.mood_by_date),
      fill: false,
      borderColor: 'blue',
      tension: 0.2
    }]
  };

  const stressData = {
    labels: Object.keys(data.stress_by_date),
    datasets: [{
      label: 'Stress Score',
      data: Object.values(data.stress_by_date),
      fill: false,
      borderColor: 'red',
      tension: 0.2
    }]
  };

  const emotionData = {
    labels: Object.keys(data.emotions),
    datasets: [{
      label: 'Emotion Count',
      data: Object.values(data.emotions),
      backgroundColor: 'purple'
    }]
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>📊 Mental Health Trends</h2>
      <h4>Mood Over Time</h4>
      <Line data={moodData} />

      <h4 style={{ marginTop: '3rem' }}>Stress Over Time</h4>
      <Line data={stressData} />

      <h4 style={{ marginTop: '3rem' }}>Emotion Distribution</h4>
      <Bar data={emotionData} />
    </div>
  );
}
