import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});


api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});


export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
};


export const ticketAPI = {
  createTicket: (data) => api.post('/tickets', data),
  getMyTickets: () => api.get('/tickets/my'),
  getAllTickets: () => api.get('/tickets'),
  resolveTicket: (ticketId) => api.put(`/tickets/${ticketId}/resolve`),
};


export const engineerAPI = {
  getEngineerTickets: () => api.get('/engineer/tickets'),
};


export const adminAPI = {
  assignTicket: (ticketId, engineerId) => 
    api.put(`/tickets/${ticketId}/assign`, { engineer_id: engineerId }),
  getReports: () => api.get('/admin/reports'),
  createNetwork: (data) => api.post('/network', data),
  getNetworks: () => api.get('/network'),
  updateNetwork: (networkId, data) => api.put(`/network/${networkId}`, data),
};

export default api;
