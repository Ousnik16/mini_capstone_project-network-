import { describe, it, expect } from 'vitest';
import { decodeJWT, extractUserFromToken } from '../utils/tokenUtils';

describe('tokenUtils', () => {
  describe('decodeJWT', () => {
    it('should decode a valid JWT token', () => {

      const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
      const payload = btoa(JSON.stringify({ role: 'admin', email: 'test@example.com' }));
      const signature = 'fakesignature';
      const token = `${header}.${payload}.${signature}`;

      const decoded = decodeJWT(token);
      expect(decoded).toEqual({ role: 'admin', email: 'test@example.com' });
    });

    it('should return null for invalid token (missing parts)', () => {
      const token = 'invalid.token';
      const decoded = decodeJWT(token);
      expect(decoded).toBeNull();
    });

    it('should return null for malformed JWT', () => {
      const token = 'invalid..token';
      const decoded = decodeJWT(token);
      expect(decoded).toBeNull();
    });

    it('should return null for token with invalid base64', () => {
      const token = 'header.!!!notbase64!!!.signature';
      const decoded = decodeJWT(token);
      expect(decoded).toBeNull();
    });
  });

  describe('extractUserFromToken', () => {
    it('should extract user info from valid token', () => {
      const header = btoa(JSON.stringify({ alg: 'HS256' }));
      const payload = btoa(JSON.stringify({ role: 'engineer', email: 'eng@example.com' }));
      const token = `${header}.${payload}.signature`;

      const user = extractUserFromToken(token, 'eng@example.com');
      expect(user).toEqual({
        email: 'eng@example.com',
        role: 'engineer',
      });
    });

    it('should default to customer role if token is invalid', () => {
      const user = extractUserFromToken('invalid', 'test@example.com');
      expect(user).toEqual({
        email: 'test@example.com',
        role: 'customer',
      });
    });

    it('should use customer role if role not in payload', () => {
      const header = btoa(JSON.stringify({ alg: 'HS256' }));
      const payload = btoa(JSON.stringify({ email: 'test@example.com' }));
      const token = `${header}.${payload}.signature`;

      const user = extractUserFromToken(token, 'test@example.com');
      expect(user).toEqual({
        email: 'test@example.com',
        role: 'customer',
      });
    });
  });
});
