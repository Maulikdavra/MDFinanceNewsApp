import React, { useState, useEffect } from 'react';
import { Paper, Title, Select, Accordion, Group, Text, Progress, Stack } from '@mantine/core';
import axios from 'axios';

export function NewsSection({ company }) {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [category, setCategory] = useState('All');

  useEffect(() => {
    const fetchNews = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`/api/news/${company}?category=${category}`);
        setNews(response.data);
        setError(null);
      } catch (err) {
        setError('Unable to fetch news');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (company) {
      fetchNews();
    }
  }, [company, category]);

  return (
    <Paper p="md" radius="md" mt="md">
      <Title order={3}>Latest News for {company}</Title>

      <Select
        data={['All', 'Technology', 'Market', 'Press Releases']}
        value={category}
        onChange={setCategory}
        label="Filter by Category"
        mt="md"
      />

      {loading ? (
        <Text>Loading news...</Text>
      ) : error ? (
        <Text color="red">{error}</Text>
      ) : news.length === 0 ? (
        <Text>No news found for {company}</Text>
      ) : (
        <Accordion mt="md">
          {news.map((article, index) => (
            <Accordion.Item key={index} value={article.title}>
              <Accordion.Control>{article.title}</Accordion.Control>
              <Accordion.Panel>
                <Stack spacing="md">
                  <Group position="apart">
                    <div>
                      <Text weight={500}>Source: {article.source}</Text>
                      <Text size="sm">Published: {article.publishedAt}</Text>
                    </div>
                    <div>
                      <Text weight={500}>Sentiment Analysis</Text>
                      <Progress 
                        value={article.sentiment.confidence * 100} 
                        label={`${(article.sentiment.confidence * 100).toFixed(0)}%`}
                      />
                      <Text>Rating: {'⭐'.repeat(article.sentiment.rating)}</Text>
                    </div>
                  </Group>

                  <Text>{article.summary}</Text>

                  <Text>
                    <a href={article.url} target="_blank" rel="noopener noreferrer">
                      Read full article
                    </a>
                  </Text>
                </Stack>
              </Accordion.Panel>
            </Accordion.Item>
          ))}
        </Accordion>
      )}
    </Paper>
  );
}
