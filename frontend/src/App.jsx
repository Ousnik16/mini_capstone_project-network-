import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Unauthorized } from './pages/Unauthorized';
import { ProtectedRoute } from './components/ProtectedRoute';
import { CustomerDashboard } from './pages/CustomerDashboard';
import { EngineerDashboard } from './pages/EngineerDashboard';
import { AdminDashboard } from './pages/AdminDashboard';
import './App.css';

function AppRoutes() {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
{}
      <Route path="/login" element={isAuthenticated ? <Navigate to="/" /> : <Login />} />
      <Route path="/register" element={isAuthenticated ? <Navigate to="/" /> : <Register />} />
      <Route path="/unauthorized" element={<Unauthorized />} />

{}
      <Route
        path="/customer/dashboard"
        element={
          <ProtectedRoute>
            <CustomerDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/engineer/dashboard"
        element={
          <ProtectedRoute>
            <EngineerDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/dashboard"
        element={
          <ProtectedRoute>
            <AdminDashboard />
          </ProtectedRoute>
        }
      />

{}
      <Route
        path="/"
        element={
          isAuthenticated ? (
            <Navigate to="/customer/dashboard" />
          ) : (
            <Navigate to="/login" />
          )
        }
      />

{}
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </Router>
  );
}

export default App;
