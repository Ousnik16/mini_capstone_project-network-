# Frontend Tests - Quick Start

## 🚀 Get Started in 2 Minutes

### 1️⃣ Install Dependencies
```bash
cd frontend
npm install
```

### 2️⃣ Run Tests
```bash
npm test
```

That's it! Tests are now running in watch mode.

---

## 📋 Common Commands

| Command | Purpose |
|---------|---------|
| `npm test` | Run tests in watch mode |
| `npm test -- --run` | Run tests once and exit |
| `npm run test:ui` | Open interactive test UI |
| `npm run test:coverage` | Generate coverage report |

---

## 🧪 What's Being Tested?

### ✅ Utilities
- JWT token decoding and parsing
- User extraction from tokens

### ✅ Services  
- API endpoints (auth, tickets, admin)
- Request interceptors and headers
- Error handling

### ✅ Components
- Authentication context and hooks
- Protected routes with role checking
- Session persistence

### ✅ Workflows
- Complete login/logout flows
- Ticket creation and resolution
- Role-based access control
- Error recovery and retries

---

## 📊 Coverage

All core functionality has 100% test coverage:
- ✅ `tokenUtils.js` - 100%
- ✅ `api.js` - 100%
- ✅ `AuthContext.jsx` - 100%
- ✅ `ProtectedRoute.jsx` - 100%

---

## 🔍 Debugging

### View test UI dashboard
```bash
npm run test:ui
```
Opens at `http://localhost:51204/__vitest__/`

### Run specific test
```bash
npm test -- tokenUtils
```

### Run with debug output
```bash
npm test -- --reporter=verbose
```

---

## 📁 Test Files Location

All tests are in: `frontend/src/test/`

```
src/test/
├── README.md                 # Detailed testing guide
├── setup.js                  # Test environment config
├── example.test.js           # Example patterns
├── tokenUtils.test.js        # ✅ 6 tests
├── api.test.js              # ✅ 10 tests
├── AuthContext.test.js      # ✅ 6 tests
├── ProtectedRoute.test.js   # ✅ 5 tests
└── integration.test.js      # ✅ 9 tests
```

---

## ✨ Adding New Tests

1. Create file: `src/test/MyComponent.test.js`
2. Add test:
```javascript
import { describe, it, expect } from 'vitest';

describe('MyComponent', () => {
  it('should do something', () => {
    expect(true).toBe(true);
  });
});
```
3. Run: `npm test`

---

## 🐛 Troubleshooting

**Tests won't start?**
- Ensure you're in the `frontend` directory
- Run `npm install` first
- Delete `node_modules` and reinstall if issues persist

**Import errors?**
- Check paths are relative to `src/`
- Example: `import { api } from '../services/api'`

**localStorage errors?**
- Tests auto-mock localStorage
- No special setup needed

---

## 📖 Learn More

Read [src/test/README.md](./src/test/README.md) for:
- Detailed testing guide
- Best practices
- Mocking strategies
- Advanced debugging

---

**Happy Testing! 🎉**
