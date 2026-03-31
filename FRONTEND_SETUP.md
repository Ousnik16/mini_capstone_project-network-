# Frontend Setup and Installation Guide

## Quick Start

### 1. Install Dependencies

Navigate to the frontend directory and install all required packages:

```bash
cd frontend
npm install
```

### 2. Configure Environment Variables

Create a `.env` file in the `frontend` directory (if not already present):

```
VITE_API_BASE_URL=http://localhost:8000
```

This tells the frontend where to connect to the backend API.

### 3. Start Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. Open in Browser

Visit: `http://localhost:5173`

You'll be redirected to the login page if not authenticated.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build locally

## User Roles and Access

### 1. Customer Account
- **Can do:**
  - Register as a customer
  - Create support tickets for network issues
  - View their own tickets and status
  - Track ticket resolution progress

- **Example credentials to register:**
  - Name: John Doe
  - Email: customer@example.com
  - Password: password123
  - Role: Select "Customer"

### 2. Engineer Account
- **Can do:**
  - View all tickets assigned to them
  - Mark tickets as resolved
  - Track their workload

- **To access:**
  - Register with role: "Engineer"
  - Admin must assign tickets to you

### 3. Admin Account
- **Can do:**
  - View all tickets in the system
  - Assign tickets to engineers
  - View system analytics and reports
  - Manage network infrastructure nodes
  - Monitor overall system health

- **To access:**
  - Register with role: "Admin"

## Project Structure Overview

```
frontend/src/
├── pages/
│   ├── Login.jsx              # Login page
│   ├── Register.jsx           # Registration page
│   ├── CustomerDashboard.jsx  # Customer interface
│   ├── EngineerDashboard.jsx  # Engineer interface
│   ├── AdminDashboard.jsx     # Admin interface
│   └── Unauthorized.jsx       # Unauthorized access page
├── components/
│   └── ProtectedRoute.jsx     # Route protection wrapper
├── contexts/
│   └── AuthContext.jsx        # Auth state management
├── services/
│   └── api.js                 # API client and endpoints
├── styles/
│   ├── Auth.css               # Authentication styles
│   └── Dashboard.css          # Dashboard styles
├── App.jsx                    # Main app with routing
├── App.css
├── main.jsx
└── index.css
```

## API Endpoints Used

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Tickets (Customers)
- `POST /tickets` - Create new ticket
- `GET /tickets/my` - Get my tickets
- `PUT /tickets/{id}/resolve` - Resolve ticket

### Tickets (Admin)
- `GET /tickets` - Get all tickets
- `PUT /tickets/{id}/assign` - Assign to engineer

### Engineer
- `GET /engineer/tickets` - Get assigned tickets

### Admin
- `GET /admin/reports` - Get system reports
- `POST /network` - Create network node
- `PUT /network/{id}` - Update network node

## Common Issues and Solutions

### Issue: API connection errors
**Solution:** Make sure the backend is running on `http://localhost:8000` and the VITE_API_BASE_URL in `.env` is correctly set.

### Issue: CORS errors
**Solution:** Ensure your backend has CORS enabled for `http://localhost:5173`

### Issue: "Module not found" errors
**Solution:** Run `npm install` again to ensure all dependencies are installed.

### Issue: Page stays loading
**Solution:** Check your browser's Network tab in DevTools to see if API calls are failing.

## Testing the Application

### Test Workflow:

1. **Register as Customer**
   - Go to `/register`
   - Fill in details and select "Customer" role
   - Click Register

2. **Create a Ticket**
   - Go to Customer Dashboard
   - Click "Create New Ticket"
   - Fill in issue type, description, and location
   - Submit

3. **Switch to Admin Account**
   - Logout and register a new admin account
   - Go to Admin Dashboard, Tickets tab

4. **Assign Ticket**
   - Select the ticket you created
   - Enter an engineer ID
   - Click "Assign Ticket"

5. **Switch to Engineer Account**
   - Logout and register as engineer
   - Go to Engineer Dashboard
   - View assigned tickets
   - Click "Mark as Resolved"

6. **Check Admin Reports**
   - Switch back to admin
   - Go to Reports tab
   - View system analytics

## Features Implemented

### Authentication & Authorization
- ✅ User registration with role selection
- ✅ User login with JWT token
- ✅ Protected routes based on authentication
- ✅ Token stored in localStorage
- ✅ Token automatically included in all API requests

### Customer Features
- ✅ Create support tickets
- ✅ View own tickets
- ✅ Filter tickets by status
- ✅ Track resolution progress

### Engineer Features
- ✅ View assigned tickets
- ✅ Mark tickets as resolved
- ✅ Track workload

### Admin Features
- ✅ View all tickets
- ✅ Assign tickets to engineers
- ✅ View system reports
- ✅ Manage network nodes
- ✅ Monitor statistics (total tickets, open, assigned, resolved)
- ✅ Track average resolution time

### UI/UX
- ✅ Responsive design
- ✅ Professional styling
- ✅ Loading states
- ✅ Error messages
- ✅ Intuitive navigation
- ✅ Dashboard layouts for each role

## Troubleshooting

### Can't connect to backend?
1. Ensure backend is running: `python -m uvicorn app.main:app --reload`
2. Check backend is on port 8000
3. Verify `.env` file has correct VITE_API_BASE_URL

### Tokens not persisting?
- Check browser's localStorage in DevTools
- Make sure localStorage is enabled
- Check token expiration settings on backend

### Page not rendering?
- Open DevTools (F12) and check Console for errors
- Check Network tab to see API responses
- Ensure all dependencies are installed: `npm install`

## Next Steps

- Consider adding more features like ticket comments/updates
- Add email notifications
- Implement real-time updates with WebSockets
- Add user profile management
- Implement ticket search and filtering
- Add data export functionality

## Support

For issues or questions, refer to the backend README or contact the development team.
