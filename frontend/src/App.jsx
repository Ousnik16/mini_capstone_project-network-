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
  const { isAuthenticated, user } = useAuth();

  const getDefaultDashboard = () => {
    if (!isAuthenticated) return "/login";
    switch (user?.role) {
      case "customer":
        return "/customer/dashboard";
      case "engineer":
        return "/engineer/dashboard";
      case "admin":
        return "/admin/dashboard";
      default:
        return "/login";
    }
  };

  return (
    <Routes>
{}
      <Route path="/login" element={isAuthenticated ? <Navigate to={getDefaultDashboard()} /> : <Login />} />
      <Route path="/register" element={isAuthenticated ? <Navigate to={getDefaultDashboard()} /> : <Register />} />
      <Route path="/unauthorized" element={<Unauthorized />} />

{}
      <Route
        path="/customer/dashboard"
        element={
          <ProtectedRoute requiredRole="customer">
            <CustomerDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/engineer/dashboard"
        element={
          <ProtectedRoute requiredRole="engineer">
            <EngineerDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/dashboard"
        element={
          <ProtectedRoute requiredRole="admin">
            <AdminDashboard />
          </ProtectedRoute>
        }
      />

{}
      <Route
        path="/"
        element={
          isAuthenticated ? (
            <Navigate to={getDefaultDashboard()} />
          ) : (
            <Navigate to="/login" />
          )
        }
      />

{}
      <Route path="*" element={<Navigate to={getDefaultDashboard()} />} />
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
