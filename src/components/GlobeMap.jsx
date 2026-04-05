import React, { useRef, useState, useEffect } from 'react';
import Globe from 'react-globe.gl';
import * as THREE from 'three';
import billionairesData from '../data/billionaires.json';

const GlobeMap = () => {
  const globeRef = useRef();
  const [dimensions, setDimensions] = useState({ width: window.innerWidth, height: window.innerHeight });

  // Add event listener for resizing
  useEffect(() => {
    const handleResize = () => {
      setDimensions({ width: window.innerWidth, height: window.innerHeight });
    };
    window.addEventListener('resize', handleResize);
    
    // Initial camera positioning
    if (globeRef.current) {
      globeRef.current.controls().autoRotate = true;
      globeRef.current.controls().autoRotateSpeed = 0.5;
      // Start focusing slightly above the equator
      globeRef.current.pointOfView({ lat: 20, lng: 0, altitude: 2.2 }, 2000);
    }
    
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Prepare data points
  // Map final worth to visual scales.
  const pointsData = billionairesData.map(b => ({
    lat: b.lat,
    lng: b.lng,
    size: Math.max(0.1, Math.min(b.netWorth / 100000, 1.5)), // Normalize size a bit
    color: '#00d2ff', // User specifically requested "blue"
    name: b.name,
    worth: b.netWorth,
    industry: b.industry,
    city: b.city,
    country: b.country
  }));

  // HTML content for tooltips
  const getTooltipHTML = (d) => `
    <div class="scene-tooltip">
      <div class="tooltip-name">${d.name}</div>
      <div class="tooltip-worth">$${(d.worth / 1000).toFixed(1)} Billion</div>
      <div class="tooltip-meta">${d.industry}</div>
      <div class="tooltip-meta">${d.city ? d.city + ', ' : ''}${d.country}</div>
    </div>
  `;

  return (
    <div className="globe-container">
      <Globe
        ref={globeRef}
        width={dimensions.width}
        height={dimensions.height}
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-night.jpg"
        backgroundImageUrl="//unpkg.com/three-globe/example/img/night-sky.png"
        pointsData={pointsData}
        pointLat="lat"
        pointLng="lng"
        pointColor="color"
        pointAltitude={d => d.size * 0.5} // Height of points based on network
        pointRadius={d => d.size * 1.5}
        pointsMerge={false}
        pointResolution={32}
        pointLabel={getTooltipHTML}
        atmosphereColor="#00d2ff"
        atmosphereAltitude={0.15}
      />
    </div>
  );
};

export default GlobeMap;
