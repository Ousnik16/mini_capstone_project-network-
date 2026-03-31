// Utility function to decode JWT token and extract payload
export const decodeJWT = (token) => {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) {
      throw new Error('Invalid token');
    }
    const decoded = JSON.parse(atob(parts[1]));
    return decoded;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

// Extract user info from JWT payload
export const extractUserFromToken = (token, email) => {
  const payload = decodeJWT(token);
  if (!payload) {
    return { email, role: 'customer' };
  }
  return {
    email,
    role: payload.role || 'customer',
  };
};
