import React, { useState, useEffect } from 'react';
import { ticketAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import '../styles/Dashboard.css';

export const CustomerDashboard = () => {
  const [tickets, setTickets] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { logout } = useAuth();
  const [formData, setFormData] = useState({
    issue_type: '',
    description: '',
    location: '',
  });

  useEffect(() => {
    fetchTickets();
  }, []);

  const fetchTickets = async () => {
    setLoading(true);
    try {
      const response = await ticketAPI.getMyTickets();
      setTickets(response.data);
      setError('');

    } catch (err) {
      setError('Failed to fetch tickets');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleCreateTicket = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await ticketAPI.createTicket(formData);
      setFormData({ issue_type: '', description: '', location: '' });
      setShowCreateForm(false);
      await fetchTickets();
      setError('');

    } catch (err) {
      setError('Failed to create ticket');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Customer Dashboard</h1>
        <button onClick={logout} className="logout-btn">Logout</button>
      </div>

      <div className="dashboard-content">
        <section className="section">
          <div className="section-header">
            <h2>Your Tickets</h2>
            <button 
              onClick={() => setShowCreateForm(!showCreateForm)}
              className="btn-primary"
            >
              {showCreateForm ? 'Cancel' : 'Create New Ticket'}
            </button>
          </div>

          {showCreateForm && (
            <div className="form-card">
              <h3>Create New Ticket</h3>
              {error && <div className="error">{error}</div>}
              <form onSubmit={handleCreateTicket}>
                <div className="form-group">
                  <label>Issue Type</label>
                  <input
                    type="text"
                    name="issue_type"
                    value={formData.issue_type}
                    onChange={handleChange}
                    required
                    placeholder="E.g., Network Down, Connection Issue"
                  />
                </div>
                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    required
                    placeholder="Describe the issue in detail"
                    rows="4"
                  />
                </div>
                <div className="form-group">
                  <label>Location</label>
                  <input
                    type="text"
                    name="location"
                    value={formData.location}
                    onChange={handleChange}
                    required
                    placeholder="Where is the issue?"
                  />
                </div>
                <button type="submit" disabled={loading}>
                  {loading ? 'Creating...' : 'Create Ticket'}
                </button>
              </form>
            </div>
          )}

          {error && !showCreateForm && <div className="error">{error}</div>}
          
          {loading && !showCreateForm ? (
            <p>Loading tickets...</p>
          ) : tickets.length === 0 ? (
            <p>No tickets found. Create one to get started!</p>
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
                  <p><strong>Description:</strong> {ticket.description}</p>
                  <p><strong>Location:</strong> {ticket.location}</p>
                  <p><strong>Created:</strong> {new Date(ticket.created_at).toLocaleString()}</p>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
};
