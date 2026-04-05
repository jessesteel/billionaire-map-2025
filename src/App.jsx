import React, { useMemo } from 'react';
import GlobeMap from './components/GlobeMap';
import billionairesData from './data/billionaires.json';

function App() {
  const stats = useMemo(() => {
    const totalWorth = billionairesData.reduce((acc, b) => acc + (b.netWorth || 0), 0);
    const topIndustry = "Technology"; // Can be computed dynamically
    return {
      count: billionairesData.length,
      totalWorth: (totalWorth / 1000).toFixed(1), // In trillions roughly if / 1000 for billions
    };
  }, []);

  return (
    <div className="app-container">
      <div className="overlay-panel">
        <div className="title-section">
          <h1>OpenGrid Wealth</h1>
          <p>Real-time geospacial mapping of the world's most concentrated capital centers.</p>
        </div>
        
        <div className="stats-grid">
          <div className="stat-box">
            <span className="stat-label">Billionaires</span>
            <span className="stat-value">{stats.count}</span>
          </div>
          <div className="stat-box">
            <span className="stat-label">Total Capital</span>
            <span className="stat-value">${stats.totalWorth}B</span>
          </div>
        </div>
      </div>
      
      <GlobeMap />
    </div>
  );
}

export default App;
