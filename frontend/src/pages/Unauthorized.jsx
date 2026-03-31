import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Auth.css';

export const Unauthorized = () => {
  const navigate = useNavigate();

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Unauthorized Access</h2>
        <p style={{ marginBottom: '20px', color: '#666' }}>
          You don't have permission to access this page.
        </p>
        <button
          onClick={() => navigate('/')}
          className="btn-primary"
          style={{ width: '100%' }}
        >
          Go to Home
        </button>
      </div>
    </div>
  );
};
