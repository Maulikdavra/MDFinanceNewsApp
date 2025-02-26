import React, { useState } from 'react';
import { Button, TextInput, Paper, Title, Stack } from '@mantine/core';

export function CompanyList({ 
  companies, 
  currentCompany, 
  onAddCompany, 
  onRemoveCompany, 
  onSelectCompany 
}) {
  const [newCompany, setNewCompany] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (newCompany.trim()) {
      onAddCompany(newCompany.trim());
      setNewCompany('');
    }
  };

  return (
    <Paper p="md" radius="md">
      <Title order={3}>Add Company</Title>
      
      <form onSubmit={handleSubmit}>
        <Stack spacing="sm">
          <TextInput
            value={newCompany}
            onChange={(e) => setNewCompany(e.target.value)}
            placeholder="Enter a company name"
          />
          <Button type="submit" fullWidth>
            Add Company
          </Button>
        </Stack>
      </form>

      {companies.length > 0 && (
        <>
          <Title order={3} mt="md">Your Companies</Title>
          <Stack spacing="xs" mt="sm">
            {companies.map((company, index) => (
              <div key={index} className="company-list-item">
                <Button
                  variant={company === currentCompany ? "filled" : "light"}
                  onClick={() => onSelectCompany(company)}
                  fullWidth
                >
                  {company}
                </Button>
                <Button
                  variant="subtle"
                  color="red"
                  compact
                  onClick={() => onRemoveCompany(company)}
                  title={`Remove ${company}`}
                >
                  🗑
                </Button>
              </div>
            ))}
          </Stack>
        </>
      )}
    </Paper>
  );
}
