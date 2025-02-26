import React, { useState, useEffect } from 'react';
import { Paper, Group, Text, Loader } from '@mantine/core';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

export function StockSection({ company }) {
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStockData = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`/api/stock/${company}`);
        setStockData(response.data);
        setError(null);
      } catch (err) {
        setError('Unable to fetch stock data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (company) {
      fetchStockData();
    }
  }, [company]);

  if (loading) {
    return <Loader />;
  }

  if (error) {
    return <Text color="red">{error}</Text>;
  }

  if (!stockData) {
    return null;
  }

  const chartData = {
    labels: Object.keys(stockData.history),
    datasets: [{
      label: 'Stock Price',
      data: Object.values(stockData.history),
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  };

  return (
    <Paper p="md" radius="md">
      <Group position="apart" mb="md">
        <div>
          <Text size="lg" weight={500}>Current Price</Text>
          <Text size="xl">${stockData.price.toFixed(2)}</Text>
          <Text color={stockData.change_percent >= 0 ? 'green' : 'red'}>
            {stockData.change_percent.toFixed(2)}%
          </Text>
        </div>
        <div>
          <Text size="lg" weight={500}>Change</Text>
          <Text size="xl">${Math.abs(stockData.change).toFixed(2)}</Text>
        </div>
        <div>
          <Text size="lg" weight={500}>Volume</Text>
          <Text size="xl">{stockData.volume.toLocaleString()}</Text>
        </div>
      </Group>

      <div style={{ height: '300px' }}>
        <Line
          data={chartData}
          options={{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              }
            }
          }}
        />
      </div>
    </Paper>
  );
}
