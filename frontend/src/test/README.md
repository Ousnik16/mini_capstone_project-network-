# Frontend Testing Guide

This guide explains how to run and maintain tests for the frontend application.

## Testing Stack

- **Vitest**: Fast unit test framework optimized for Vite projects
- **React Testing Library**: Component testing utilities
- **jsdom**: JavaScript implementation of web standards for Node.js

## Setup

Testing dependencies have been added to `package.json`. Install them with:

```bash
npm install
```

## Running Tests

### Run all tests
```bash
npm test
```

### Run tests in watch mode
```bash
npm test -- --watch
```

### Run tests with UI
```bash
npm run test:ui
```

### Generate coverage report
```bash
npm run test:coverage
```

## Test Files

### Unit Tests

- **`tokenUtils.test.js`** - JWT token decoding and user extraction utilities
  - Tests for valid/invalid token parsing
  - User role extraction from tokens
  - Default role fallback

- **`api.test.js`** - API service layer
  - Auth endpoints (register, login)
  - Ticket operations (create, get, resolve)
  - Engineer API calls
  - Admin operations (assign, reports, network)
  - Request interceptor behavior

### Component Tests

- **`AuthContext.test.js`** - Authentication context provider
  - Session restoration from localStorage
  - Login/logout functionality
  - Context hook usage
  - Error handling when used outside provider

- **`ProtectedRoute.test.js`** - Protected route component
  - Renders protected content when authenticated
  - Redirects to login when not authenticated
  - Role-based access control
  - Unauthorized redirect for insufficient permissions

## Test Structure

Each test file follows this pattern:

```javascript
import { describe, it, expect, beforeEach, vi } from 'vitest';

describe('Feature/Component', () => {
  beforeEach(() => {
    // Setup
  });

  it('should do something specific', () => {
    // Arrange
    // Act
    // Assert
  });
});
```

## Mocking

### localStorage Mock
Located in `src/test/setup.js`:
```javascript
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};
```

### API Mock
Use Vitest's `vi.mock()` for axios interceptor testing:
```javascript
vi.mock('axios');
api.post = vi.fn().mockResolvedValue({ data: {...} });
```

## Writing New Tests

1. Create a new file in `src/test/` with `.test.js` extension
2. Import necessary testing utilities:
   ```javascript
   import { describe, it, expect, beforeEach, vi } from 'vitest';
   import { render, screen } from '@testing-library/react';
   ```
3. Write tests following the AAA pattern (Arrange, Act, Assert)
4. Use proper cleanup with `beforeEach()` and `afterEach()`

## Best Practices

- ✅ Test behavior, not implementation
- ✅ Use descriptive test names
- ✅ Keep tests focused and isolated
- ✅ Mock external dependencies (API calls, localStorage)
- ✅ Clean up after each test
- ❌ Avoid testing implementation details
- ❌ Don't create interdependent tests
- ❌ Avoid magic numbers - use named constants

## Coverage Goals

Aim for at least 80% code coverage:
- Statements: 80%
- Branches: 75%
- Functions: 80%
- Lines: 80%

## Debugging Tests

### Run single test file
```bash
npm test -- tokenUtils.test.js
```

### Run tests matching pattern
```bash
npm test -- --grep "AuthContext"
```

### Enable debug output
```javascript
import { screen, debug } from '@testing-library/react';

debug(); // Prints DOM snapshot
```

## Common Issues

### localStorage is not defined
- Tests use a mock localStorage. Ensure `src/test/setup.js` is included in `vitest.config.js`

### Component not rendering
- Check that components are wrapped in required providers (AuthProvider, Router)
- Verify test async operations with `waitFor()`

### API calls failing in tests
- Mock the axios instance before importing the API module
- Use `vi.mock('axios')` at the top of test files

## Future Improvements

- Add E2E tests with Playwright or Cypress
- Increase test coverage for page components
- Add visual regression testing
- Set up CI/CD integration for automated testing
