import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

const ChartComponent = ({ data }) => {
  const emotionValues = {
    H: 4,
    D: 1,
    ST: 2,
    A: 3,
  };
  const dates = data.map((item) => new Date(item.date).toLocaleTimeString());
  const emotions = data.map((item) => emotionValues[item.emotion]);
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );
  const chartData = {
    labels: dates,
    datasets: [
      {
        label: "Emotions",
        data: emotions,
        fill: false,
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      },
    ],
  };
  const option = {
    scales: {
      x: {
        type: "category",
      },
    },
  };

  return (
    <div>
      <h2>Emotions Over Time</h2>
      <Line data={chartData} options={option} />
    </div>
  );
};

export default ChartComponent;
