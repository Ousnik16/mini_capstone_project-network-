/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from 'react';
import { engineerAPI, ticketAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import '../styles/Dashboard.css';

export const EngineerDashboard = () => {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [resolvingId, setResolvingId] = useState(null);
  const { logout } = useAuth();

  useEffect(() => {
    fetchTickets();
  }, []);

  const fetchTickets = async () => {
    setLoading(true);
    try {
      const response = await engineerAPI.getEngineerTickets();
      setTickets(response.data);
      setError('');
    // eslint-disable-next-line no-unused-vars
    } catch (err) {
      setError('Failed to fetch tickets');
    } finally {
      setLoading(false);
    }
  };

  const handleResolveTicket = async (ticketId) => {
    setResolvingId(ticketId);
    try {
      await ticketAPI.resolveTicket(ticketId);
      await fetchTickets();
      setError('');
    } catch (err) {
      setError('Failed to resolve ticket');
    } finally {
      setResolvingId(null);
    }
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Engineer Dashboard</h1>
        <button onClick={logout} className="logout-btn">Logout</button>
      </div>

      <div className="dashboard-content">
        <section className="section">
          <div className="section-header">
            <h2>Assigned Tickets</h2>
          </div>

          {error && <div className="error">{error}</div>}
          
          {loading ? (
            <p>Loading tickets...</p>
          ) : tickets.length === 0 ? (
            <p>No tickets assigned to you yet.</p>
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
                  
                  {ticket.status !== 'resolved' && (
                    <button
                      onClick={() => handleResolveTicket(ticket.id)}
                      disabled={resolvingId === ticket.id}
                      className="btn-resolve"
                    >
                      {resolvingId === ticket.id ? 'Resolving...' : 'Mark as Resolved'}
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
};
