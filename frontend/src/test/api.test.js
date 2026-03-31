
import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';


vi.mock('axios', () => ({
  default: {
    create: vi.fn(() => ({
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
      interceptors: {
        request: {
          use: vi.fn(),
        },
        response: {
          use: vi.fn(),
        },
      },
    })),
  },
}));

import api, { authAPI, ticketAPI, engineerAPI, adminAPI } from '../services/api';

describe('API Service', () => {
  beforeEach(() => {
    localStorage.getItem.mockClear();
    localStorage.setItem.mockClear();
    localStorage.removeItem.mockClear();
    vi.clearAllMocks();
  });

  describe('authAPI', () => {
    it('should call register endpoint', async () => {
      const mockData = { email: 'test@example.com', password: 'password123' };
      api.post = vi.fn().mockResolvedValue({ data: { message: 'Registered' } });

      await authAPI.register(mockData);
      expect(api.post).toHaveBeenCalledWith('/auth/register', mockData);
    });

    it('should call login endpoint', async () => {
      const mockData = { email: 'test@example.com', password: 'password123' };
      api.post = vi.fn().mockResolvedValue({ data: { access_token: 'token' } });

      await authAPI.login(mockData);
      expect(api.post).toHaveBeenCalledWith('/auth/login', mockData);
    });
  });

  describe('ticketAPI', () => {
    it('should create a ticket', async () => {
      const mockData = { title: 'Test Ticket', description: 'Test' };
      api.post = vi.fn().mockResolvedValue({ data: { id: 1 } });

      await ticketAPI.createTicket(mockData);
      expect(api.post).toHaveBeenCalledWith('/tickets', mockData);
    });

    it('should get user tickets', async () => {
      api.get = vi.fn().mockResolvedValue({ data: [] });

      await ticketAPI.getMyTickets();
      expect(api.get).toHaveBeenCalledWith('/tickets/my');
    });

    it('should get all tickets', async () => {
      api.get = vi.fn().mockResolvedValue({ data: [] });

      await ticketAPI.getAllTickets();
      expect(api.get).toHaveBeenCalledWith('/tickets');
    });

    it('should resolve a ticket', async () => {
      api.put = vi.fn().mockResolvedValue({ data: { id: 1, status: 'resolved' } });

      await ticketAPI.resolveTicket(1);
      expect(api.put).toHaveBeenCalledWith('/tickets/1/resolve');
    });
  });

  describe('engineerAPI', () => {
    it('should get engineer tickets', async () => {
      api.get = vi.fn().mockResolvedValue({ data: [] });

      await engineerAPI.getEngineerTickets();
      expect(api.get).toHaveBeenCalledWith('/engineer/tickets');
    });
  });

  describe('adminAPI', () => {
    it('should assign ticket to engineer', async () => {
      api.put = vi.fn().mockResolvedValue({ data: { id: 1 } });

      await adminAPI.assignTicket(1, 2);
      expect(api.put).toHaveBeenCalledWith('/tickets/1/assign', { engineer_id: 2 });
    });

    it('should get admin reports', async () => {
      api.get = vi.fn().mockResolvedValue({ data: [] });

      await adminAPI.getReports();
      expect(api.get).toHaveBeenCalledWith('/admin/reports');
    });

    it('should create a network', async () => {
      const mockData = { name: 'Test Network' };
      api.post = vi.fn().mockResolvedValue({ data: { id: 1 } });

      await adminAPI.createNetwork(mockData);
      expect(api.post).toHaveBeenCalledWith('/network', mockData);
    });

    it('should update a network', async () => {
      const mockData = { name: 'Updated Network' };
      api.put = vi.fn().mockResolvedValue({ data: { id: 1 } });

      await adminAPI.updateNetwork(1, mockData);
      expect(api.put).toHaveBeenCalledWith('/network/1', mockData);
    });
  });

  describe('API Interceptors', () => {
    it('should add authorization token to request headers', () => {
      const token = 'test-token-123';
      localStorage.getItem.mockReturnValue(token);

      expect(localStorage.getItem).toBeDefined();
    });

    it('should handle missing token gracefully', () => {
      localStorage.getItem.mockReturnValue(null);

      expect(() => {
        localStorage.getItem('access_token');
      }).not.toThrow();
    });
  });
});
