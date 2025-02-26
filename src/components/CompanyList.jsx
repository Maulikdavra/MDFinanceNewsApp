import React, { useState } from 'react';
import { Button, TextInput, Paper, Title, Stack, ActionIcon, Tooltip } from '@mantine/core';
import { IconTrash } from '@tabler/icons-react';

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
                <Tooltip label={`Remove ${company}`} position="right">
                  <ActionIcon
                    variant="subtle"
                    color="red"
                    onClick={() => onRemoveCompany(company)}
                    size="lg"
                  >
                    <IconTrash size="1.2rem" />
                  </ActionIcon>
                </Tooltip>
              </div>
            ))}
          </Stack>
        </>
      )}
    </Paper>
  );
}