# Telecom Fault Management System - Frontend

A modern React-based frontend for managing telecommunications network faults and support tickets.

## Features

- **Authentication**: User registration and login with role-based access control
- **Customer Portal**: Create and track support tickets for network issues
- **Engineer Dashboard**: View assigned tickets and mark them as resolved
- **Admin Dashboard**: 
  - Manage all tickets in the system
  - Assign tickets to engineers
  - View system reports and analytics
  - Manage network infrastructure nodes

## Project Structure

```
frontend/
├── public/              # Static files
├── src/
│   ├── components/      # Reusable React components
│   ├── contexts/        # React context for state management (Auth)
│   ├── pages/           # Page components
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── CustomerDashboard.jsx
│   │   ├── EngineerDashboard.jsx
│   │   └── AdminDashboard.jsx
│   ├── services/        # API services
│   │   └── api.js       # Axios instance and API endpoints
│   ├── styles/          # CSS files
│   │   ├── Auth.css
│   │   └── Dashboard.css
│   ├── App.jsx          # Main app component with routing
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── .env                 # Environment variables
├── index.html
├── package.json
└── vite.config.js
```

## Installation

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
Create a `.env` file in the frontend directory with:
```
VITE_API_BASE_URL=http://localhost:8000
```

## Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Build

Build for production:
```bash
npm run build
```

## Routes

- `/login` - User login page
- `/register` - User registration page
- `/customer/dashboard` - Customer dashboard (protected)
- `/engineer/dashboard` - Engineer dashboard (protected)
- `/admin/dashboard` - Admin dashboard (protected)

## Authentication

The frontend uses JWT tokens stored in localStorage for authentication. The token is automatically included in API requests via axios interceptors.

## API Integration

The frontend connects to the backend API defined in `src/services/api.js`. All API calls are authenticated with the JWT token obtained during login.

### Available API Functions

#### Auth
- `authAPI.register(data)` - Register a new user
- `authAPI.login(data)` - Login user

#### Tickets
- `ticketAPI.createTicket(data)` - Create a new ticket
- `ticketAPI.getMyTickets()` - Get tickets created by current user
- `ticketAPI.getAllTickets()` - Get all tickets (admin only)
- `ticketAPI.resolveTicket(ticketId)` - Mark ticket as resolved

#### Engineer
- `engineerAPI.getEngineerTickets()` - Get assigned tickets

#### Admin
- `adminAPI.assignTicket(ticketId, engineerId)` - Assign ticket to engineer
- `adminAPI.getReports()` - Get system reports
- `adminAPI.createNetwork(data)` - Create network node
- `adminAPI.updateNetwork(networkId, data)` - Update network node

## Technologies Used

- React 19.2.4
- React Router DOM 6.20.0
- Axios 1.6.0
- Vite 8.0.1

## License

This project is part of a mini capstone project for telecommunications network fault management.
