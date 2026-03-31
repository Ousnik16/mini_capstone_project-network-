import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { render, screen} from '@testing-library/react';
import { AuthProvider, useAuth } from '../contexts/AuthContext';
import React from 'react';

// Test component that uses the auth hook
const TestComponent = () => {
  const { user, token, isAuthenticated, login, logout, register } = useAuth();
  return (
    <div>
      <div data-testid="auth-status">{isAuthenticated ? 'authenticated' : 'not-authenticated'}</div>
      <div data-testid="user-email">{user?.email || 'no-user'}</div>
      <div data-testid="token">{token || 'no-token'}</div>
      <button onClick={() => login({ email: 'test@example.com', role: 'customer' }, 'token123')}>
        Login
      </button>
      <button onClick={() => register({ email: 'new@example.com', role: 'engineer' }, 'token456')}>
        Register
      </button>
      <button onClick={() => logout()}>Logout</button>
    </div>
  );
};

describe('AuthContext', () => {
  beforeEach(() => {
    localStorage.getItem.mockClear();
    localStorage.setItem.mockClear();
    localStorage.removeItem.mockClear();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('should provide auth context', () => {
    localStorage.getItem.mockReturnValue(null);
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByTestId('auth-status')).toHaveTextContent('not-authenticated');
    expect(screen.getByTestId('user-email')).toHaveTextContent('no-user');
  });

  it('should throw error when useAuth is used outside AuthProvider', () => {
    const TestComponentWithoutProvider = () => {
      const { user } = useAuth();
      return <div>{user?.email}</div>;
    };

    expect(() => {
      render(<TestComponentWithoutProvider />);
    }).toThrow('useAuth must be used within AuthProvider');
  });

  it('should restore session from localStorage on mount', () => {
    const storedUser = { email: 'stored@example.com', role: 'admin' };
    const storedToken = 'stored-token';

    localStorage.getItem.mockImplementation((key) => {
      if (key === 'user') return JSON.stringify(storedUser);
      if (key === 'access_token') return storedToken;
      return null;
    });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByTestId('auth-status')).toHaveTextContent('authenticated');
    expect(screen.getByTestId('user-email')).toHaveTextContent('stored@example.com');
  });

  it('should call useAuth context', () => {
    // Reset localStorage mock
    localStorage.getItem.mockClear();
    localStorage.getItem.mockReturnValue(null);

    const TestHook = () => {
      const context = useAuth();
      return (
        <div>
          <span>{context.isAuthenticated ? 'Auth' : 'NoAuth'}</span>
        </div>
      );
    };

    render(
      <AuthProvider>
        <TestHook />
      </AuthProvider>
    );

    expect(screen.getByText('NoAuth')).toBeInTheDocument();
  });
});
