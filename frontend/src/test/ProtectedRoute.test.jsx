import { describe, it, expect, beforeEach} from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ProtectedRoute } from '../components/ProtectedRoute';
import { AuthProvider } from '../contexts/AuthContext';
import React from 'react';

const TestPage = () => <div>Protected Content</div>;

const renderWithRouter = (component) => {
  return render(
    <Router>
      {component}
    </Router>
  );
};

describe('ProtectedRoute', () => {
  beforeEach(() => {
    localStorage.getItem.mockClear();
    localStorage.setItem.mockClear();
    localStorage.removeItem.mockClear();
  });

  it('should render children when user is authenticated', () => {
    const storedUser = { email: 'test@example.com', role: 'customer' };
    const storedToken = 'test-token';

    localStorage.getItem.mockImplementation((key) => {
      if (key === 'user') return JSON.stringify(storedUser);
      if (key === 'access_token') return storedToken;
      return null;
    });

    renderWithRouter(
      <AuthProvider>
        <ProtectedRoute>
          <TestPage />
        </ProtectedRoute>
      </AuthProvider>
    );

    expect(screen.getByText('Protected Content')).toBeInTheDocument();
  });

  it('should redirect to login when user is not authenticated', () => {
    localStorage.getItem.mockReturnValue(null);

    renderWithRouter(
      <AuthProvider>
        <ProtectedRoute>
          <TestPage />
        </ProtectedRoute>
      </AuthProvider>
    );

    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
  });

  it('should redirect to unauthorized when user role does not match required role', () => {
    const storedUser = { email: 'test@example.com', role: 'customer' };
    const storedToken = 'test-token';

    localStorage.getItem.mockImplementation((key) => {
      if (key === 'user') return JSON.stringify(storedUser);
      if (key === 'access_token') return storedToken;
      return null;
    });

    renderWithRouter(
      <AuthProvider>
        <ProtectedRoute requiredRole="admin">
          <TestPage />
        </ProtectedRoute>
      </AuthProvider>
    );

    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
  });

  it('should render children when user role matches required role', () => {
    const storedUser = { email: 'admin@example.com', role: 'admin' };
    const storedToken = 'admin-token';

    localStorage.getItem.mockImplementation((key) => {
      if (key === 'user') return JSON.stringify(storedUser);
      if (key === 'access_token') return storedToken;
      return null;
    });

    renderWithRouter(
      <AuthProvider>
        <ProtectedRoute requiredRole="admin">
          <TestPage />
        </ProtectedRoute>
      </AuthProvider>
    );

    expect(screen.getByText('Protected Content')).toBeInTheDocument();
  });
});
