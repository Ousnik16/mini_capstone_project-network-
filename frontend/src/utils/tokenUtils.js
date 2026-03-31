
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
