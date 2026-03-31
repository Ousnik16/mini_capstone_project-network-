/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from 'react';
import { ticketAPI, adminAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import '../styles/Dashboard.css';

export const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('tickets');
  const [tickets, setTickets] = useState([]);
  const [reports, setReports] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { logout } = useAuth();
  
  // Assign ticket state
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [engineerId, setEngineerId] = useState('');
  const [assigning, setAssigning] = useState(false);

  // Network state
  const [showNetworkForm, setShowNetworkForm] = useState(false);
  const [networkFormData, setNetworkFormData] = useState({
    tower_id: '',
    location: '',
    status: 'active',
  });

  useEffect(() => {
    if (activeTab === 'tickets') {
      fetchTickets();
    } else if (activeTab === 'reports') {
      fetchReports();
    }
  }, [activeTab]);

  const fetchTickets = async () => {
    setLoading(true);
    try {
      const response = await ticketAPI.getAllTickets();
      setTickets(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch tickets');
    } finally {
      setLoading(false);
    }
  };

  const fetchReports = async () => {
    setLoading(true);
    try {
      const response = await adminAPI.getReports();
      setReports(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch reports');
    } finally {
      setLoading(false);
    }
  };

  const handleAssignTicket = async (e) => {
    e.preventDefault();
    if (!selectedTicket || !engineerId) {
      setError('Please select a ticket and enter engineer ID');
      return;
    }

    setAssigning(true);
    try {
      await adminAPI.assignTicket(selectedTicket, engineerId);
      setSelectedTicket(null);
      setEngineerId('');
      await fetchTickets();
      setError('');
    } catch (err) {
      setError('Failed to assign ticket');
    } finally {
      setAssigning(false);
    }
  };

  const handleNetworkChange = (e) => {
    const { name, value } = e.target;
    setNetworkFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleCreateNetwork = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await adminAPI.createNetwork(networkFormData);
      setNetworkFormData({ tower_id: '', location: '', status: 'active' });
      setShowNetworkForm(false);
      setError('');
    } catch (err) {
      setError('Failed to create network node');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Admin Dashboard</h1>
        <button onClick={logout} className="logout-btn">Logout</button>
      </div>

      <div className="dashboard-content">
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'tickets' ? 'active' : ''}`}
            onClick={() => setActiveTab('tickets')}
          >
            Tickets
          </button>
          <button
            className={`tab ${activeTab === 'reports' ? 'active' : ''}`}
            onClick={() => setActiveTab('reports')}
          >
            Reports
          </button>
          <button
            className={`tab ${activeTab === 'network' ? 'active' : ''}`}
            onClick={() => setActiveTab('network')}
          >
            Network
          </button>
        </div>

        {error && <div className="error">{error}</div>}

        {activeTab === 'tickets' && (
          <section className="section">
            <h2>All Tickets</h2>
            
            <div className="assign-form">
              <h3>Assign Ticket to Engineer</h3>
              <form onSubmit={handleAssignTicket}>
                <div className="form-group">
                  <label>Select Ticket</label>
                  <select
                    value={selectedTicket}
                    onChange={(e) => setSelectedTicket(e.target.value)}
                    required
                  >
                    <option value="">Choose a ticket...</option>
                    {tickets
                      .filter(t => t.status !== 'resolved')
                      .map(ticket => (
                        <option key={ticket.id} value={ticket.id}>
                          {ticket.issue_type} - {ticket.location}
                        </option>
                      ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Engineer ID</label>
                  <input
                    type="text"
                    value={engineerId}
                    onChange={(e) => setEngineerId(e.target.value)}
                    required
                    placeholder="Enter engineer ID"
                  />
                </div>
                <button type="submit" disabled={assigning}>
                  {assigning ? 'Assigning...' : 'Assign Ticket'}
                </button>
              </form>
            </div>

            {loading ? (
              <p>Loading tickets...</p>
            ) : tickets.length === 0 ? (
              <p>No tickets found.</p>
            ) : (
              <div className="tickets-list">
                {tickets.map(ticket => (
                  <div key={ticket.id} className="ticket-card">
                    <div className="ticket-header">
                      <h3>{ticket.issue_type}</h3>
                      <span className={`status ${ticket.status.toLowerCase()}`}>
                        {ticket.status}
                      </span>
                    </div>
                    <p><strong>Customer ID:</strong> {ticket.user_id}</p>
                    <p><strong>Description:</strong> {ticket.description}</p>
                    <p><strong>Location:</strong> {ticket.location}</p>
                    <p><strong>Created:</strong> {new Date(ticket.created_at).toLocaleString()}</p>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}

        {activeTab === 'reports' && (
          <section className="section">
            <h2>System Reports</h2>
            {loading ? (
              <p>Loading reports...</p>
            ) : reports ? (
              <div className="reports-grid">
                <div className="report-card">
                  <h3>Total Tickets</h3>
                  <p className="report-value">{reports.total_tickets}</p>
                </div>
                <div className="report-card">
                  <h3>Open Tickets</h3>
                  <p className="report-value">{reports.open_tickets}</p>
                </div>
                <div className="report-card">
                  <h3>Assigned Tickets</h3>
                  <p className="report-value">{reports.assigned_tickets}</p>
                </div>
                <div className="report-card">
                  <h3>Resolved Tickets</h3>
                  <p className="report-value">{reports.resolved_tickets}</p>
                </div>
                <div className="report-card">
                  <h3>Avg Resolution Time</h3>
                  <p className="report-value">
                    {Math.round(reports.avg_resolution_seconds / 60)} min
                  </p>
                </div>
              </div>
            ) : (
              <p>No reports available.</p>
            )}
          </section>
        )}

        {activeTab === 'network' && (
          <section className="section">
            <h2>Network Management</h2>
            <button
              onClick={() => setShowNetworkForm(!showNetworkForm)}
              className="btn-primary"
            >
              {showNetworkForm ? 'Cancel' : 'Add Network Node'}
            </button>

            {showNetworkForm && (
              <div className="form-card">
                <h3>Create Network Node</h3>
                <form onSubmit={handleCreateNetwork}>
                  <div className="form-group">
                    <label>Tower ID</label>
                    <input
                      type="text"
                      name="tower_id"
                      value={networkFormData.tower_id}
                      onChange={handleNetworkChange}
                      required
                      placeholder="Enter tower ID"
                    />
                  </div>
                  <div className="form-group">
                    <label>Location</label>
                    <input
                      type="text"
                      name="location"
                      value={networkFormData.location}
                      onChange={handleNetworkChange}
                      required
                      placeholder="Enter location"
                    />
                  </div>
                  <div className="form-group">
                    <label>Status</label>
                    <select
                      name="status"
                      value={networkFormData.status}
                      onChange={handleNetworkChange}
                    >
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                      <option value="maintenance">Maintenance</option>
                    </select>
                  </div>
                  <button type="submit" disabled={loading}>
                    {loading ? 'Creating...' : 'Create Network Node'}
                  </button>
                </form>
              </div>
            )}
          </section>
        )}
      </div>
    </div>
  );
};
