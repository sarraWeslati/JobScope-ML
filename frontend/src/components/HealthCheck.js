import React, { useState, useEffect } from 'react';

const HealthCheck = () => {
  const [status, setStatus] = useState('Testing...');
  const [color, setColor] = useState('#999');

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';
        console.log(`Testing backend at: ${apiUrl}/api/health`);
        
        const response = await fetch(`${apiUrl}/api/health`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });

        if (response.ok) {
          setStatus('✅ Backend is ONLINE');
          setColor('#4CAF50');
        } else {
          setStatus(`❌ Backend responded with status ${response.status}`);
          setColor('#f44336');
        }
      } catch (error) {
        setStatus(`❌ Backend is OFFLINE: ${error.message}`);
        setColor('#f44336');
        console.error('Backend error:', error);
      }
    };

    checkBackend();
    // Check every 5 seconds
    const interval = setInterval(checkBackend, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{
      padding: '20px',
      backgroundColor: '#f5f5f5',
      borderRadius: '8px',
      marginBottom: '20px',
      textAlign: 'center'
    }}>
      <h3>Backend Status</h3>
      <p style={{ color, fontSize: '18px', fontWeight: 'bold' }}>
        {status}
      </p>
      <p style={{ fontSize: '12px', color: '#666' }}>
        API URL: {process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api
      </p>
    </div>
  );
};

export default HealthCheck;
