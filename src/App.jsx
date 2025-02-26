import React, { useState, useEffect } from 'react';
import { MantineProvider } from '@mantine/core';
import { CompanyList } from './components/CompanyList';
import { NewsSection } from './components/NewsSection';
import { StockSection } from './components/StockSection';
import './styles/App.css';

function App() {
  const [selectedCompanies, setSelectedCompanies] = useState([]);
  const [currentCompany, setCurrentCompany] = useState(null);

  const handleAddCompany = (company) => {
    if (selectedCompanies.length >= 5) {
      alert("Maximum 5 companies can be added. Please remove some to add more.");
      return;
    }
    if (!selectedCompanies.includes(company)) {
      setSelectedCompanies([...selectedCompanies, company]);
    }
  };

  const handleRemoveCompany = (company) => {
    setSelectedCompanies(selectedCompanies.filter(c => c !== company));
    if (currentCompany === company) {
      setCurrentCompany(null);
    }
  };

  return (
    <MantineProvider withGlobalStyles withNormalizeCSS>
      <div className="app">
        <header className="header">
          <h1>📈 MDFinance</h1>
          <p className="subtitle">Your AI-Powered Financial News Hub</p>
        </header>
        
        <div className="main-content">
          <div className="sidebar">
            <CompanyList
              companies={selectedCompanies}
              currentCompany={currentCompany}
              onAddCompany={handleAddCompany}
              onRemoveCompany={handleRemoveCompany}
              onSelectCompany={setCurrentCompany}
            />
          </div>
          
          <div className="content">
            {currentCompany ? (
              <>
                <StockSection company={currentCompany} />
                <NewsSection company={currentCompany} />
              </>
            ) : (
              <div className="empty-state">
                Select a company from the list to view its news and stock information
              </div>
            )}
          </div>
        </div>
      </div>
    </MantineProvider>
  );
}

export default App;
