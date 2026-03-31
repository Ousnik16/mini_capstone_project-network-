# Frontend Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     REACT FRONTEND                           │
│                  (Port 5173 - Vite Dev)                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   BrowserRouter                      │   │
│  │           (React Router - Client Routing)            │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                   │
│         ┌─────────────────┼─────────────────┐                │
│         │                 │                 │                │
│    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐            │
│    │ Login   │      │Register │      │Dashbrd  │            │
│    │ Page    │      │ Page    │      │Routes   │            │
│    └─────────┘      └─────────┘      └────┬────┘            │
│                                            │                 │
│         ┌──────────────────────────────────┼──────────┐      │
│         │                                  │          │      │
│    ┌────▼──────────┐  ┌────────────────┐  │  ┌──────▼──┐   │
│    │   Customer    │  │   Engineer     │  │  │  Admin   │   │
│    │  Dashboard    │  │  Dashboard     │  │  │Dashboard │   │
│    └───────────────┘  └────────────────┘  │  └──────────┘   │
│                                            │                 │
│  ┌──────────────────────────────────────┐ │                 │
│  │          AuthContext Provider         │ │                 │
│  │  - Manages JWT token                  │ │                 │
│  │  - Stores user data                   │ │                 │
│  │  - Handles login/logout               │ │                 │
│  └──────────────────────────────────────┘ │                 │
│                                            │                 │
│  ┌──────────────────────────────────────┐ │                 │
│  │       Protected Route Component       │ │                 │
│  │  - Checks authentication              │ │                 │
│  │  - Enforces route protection          │ │                 │
│  └──────────────────────────────────────┘ │                 │
│                                            │                 │
│  ┌──────────────────────────────────────┐ │                 │
│  │         Axios API Client             │ │                 │
│  │  - Base URL: http://localhost:8000   │ │                 │
│  │  - Auto-injects JWT tokens           │ │                 │
│  │  - Handles all API calls             │ │                 │
│  └──────────────────────────────────────┘ │                 │
│                                            │                 │
└────────────────────────────────────────────┼───────────────┘
                                             │
                            HTTP/HTTPS       │   Axios
                                             │
                ┌────────────────────────────▼─────────────────┐
                │    BACKEND API SERVER                        │
                │   (Port 8000 - FastAPI)                      │
                ├────────────────────────────────────────────┐ │
                │  /auth          /tickets    /engineer      │ │
                │  /network       /admin      /reports       │ │
                └────────────────────────────────────────────┘ │
                │                                               │
                └───────────────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   MongoDB       │
                    │   Database      │
                    └─────────────────┘
```

## Component Hierarchy

```
App
├── Router
│   ├── Routes
│   │   ├── /login → Login
│   │   ├── /register → Register
│   │   ├── /unauthorized → Unauthorized
│   │   └── Protected Routes
│   │       ├── /customer/dashboard → CustomerDashboard
│   │       ├── /engineer/dashboard → EngineerDashboard
│   │       └── /admin/dashboard → AdminDashboard
│   │
│   └── AuthProvider
│       └── Manages Auth State
│           ├── user
│           ├── token
│           ├── isAuthenticated
│           └── Auth Methods
│               ├── login()
│               ├── logout()
│               └── register()
```

## Data Flow

### 1. Authentication Flow
```
User Input (Email/Password)
        │
        ▼
Register/Login Page
        │
        ▼
API Call (authAPI.register/login)
        │
        ▼
Backend Validation
        │
        ├─ Success ─┐
        │           ├─ JWT Token
        │           └─ User Data
        │
        ▼
AuthContext.login()
        │
        ├─ Save to localStorage
        ├─ Update AuthContext state
        └─ Add token to axios headers
        │
        ▼
Redirect to Dashboard
```

### 2. Ticket Creation Flow (Customer)
```
Customer Dashboard
        │
        ▼
Click "Create Ticket"
        │
        ▼
Form Input
        │
        ├─ Issue Type
        ├─ Description
        └─ Location
        │
        ▼
API Call (ticketAPI.createTicket)
        │
        ├─ Axios adds Authorization header
        └─ Sends to /tickets endpoint
        │
        ▼
Backend Creates Ticket
        │
        ├─ Validates data
        ├─ Stores in MongoDB
        └─ Returns TicketResponse
        │
        ▼
Frontend Updates UI
        │
        ├─ Show success message
        ├─ Refresh ticket list
        └─ Clear form
```

### 3. Ticket Assignment Flow (Admin)
```
Admin Dashboard → Tickets Tab
        │
        ▼
Select Ticket to Assign
        │
        ├─ Drop down shows open tickets
        └─ Select from list
        │
        ▼
Enter Engineer ID
        │
        ▼
Click "Assign Ticket"
        │
        ▼
API Call (adminAPI.assignTicket)
        │
        ├─ Send: ticketId + engineerId
        └─ Endpoint: PUT /tickets/{id}/assign
        │
        ▼
Backend Processes Assignment
        │
        ├─ Find ticket
        ├─ Assign to engineer
        └─ Return AssignmentResponse
        │
        ▼
Update UI
        │
        ├─ Show confirmation
        ├─ Refresh ticket list
        └─ Show new status
```

### 4. Report Generation Flow (Admin)
```
Admin Dashboard → Reports Tab
        │
        ▼
Load Component
        │
        ▼
API Call (adminAPI.getReports)
        │
        │   GET /admin/reports
        │
        ▼
Backend Aggregates Data
        │
        ├─ Count total tickets
        ├─ Count open tickets
        ├─ Count assigned
        ├─ Count resolved
        └─ Calculate avg resolution time
        │
        ▼
Return AdminReportResponse
        │
        ├─ total_tickets: int
        ├─ open_tickets: int
        ├─ assigned_tickets: int
        ├─ resolved_tickets: int
        └─ avg_resolution_seconds: float
        │
        ▼
Display Card Grid
        │
        ├─ Total Tickets: 45
        ├─ Open: 12
        ├─ Assigned: 28
        ├─ Resolved: 5
        └─ Avg Time: 120 min
```

## State Management

### Global State (AuthContext)
```javascript
{
  user: {
    id: string
    name: string
    email: string
    role: 'customer' | 'engineer' | 'admin'
    is_active: boolean
  },
  token: string,
  isAuthenticated: boolean,
  loading: boolean,
  methods: {
    login(userData, token)
    logout()
    register(userData, token)
  }
}
```

### Local Component State Examples

**CustomerDashboard:**
```javascript
{
  tickets: TicketResponse[],
  formData: {
    issue_type: string,
    description: string,
    location: string
  },
  showCreateForm: boolean,
  loading: boolean,
  error: string
}
```

**AdminDashboard:**
```javascript
{
  activeTab: 'tickets' | 'reports' | 'network',
  tickets: TicketResponse[],
  reports: AdminReportResponse,
  selectedTicket: string,
  engineerId: string,
  networkFormData: {
    tower_id: string,
    location: string,
    status: string
  },
  showNetworkForm: boolean,
  loading: boolean,
  error: string
}
```

## API Layer Structure

```
services/api.js
├── Axios Instance
│   ├── Base URL: http://localhost:8000
│   ├── Headers: Content-Type: application/json
│   └── Interceptors
│       └── Request: Add Authorization header
│
├── Auth Module
│   ├── register(data)
│   └── login(data)
│
├── Ticket Module
│   ├── createTicket(data)
│   ├── getMyTickets()
│   ├── getAllTickets()
│   └── resolveTicket(ticketId)
│
├── Engineer Module
│   └── getEngineerTickets()
│
└── Admin Module
    ├── assignTicket(ticketId, engineerId)
    ├── getReports()
    ├── createNetwork(data)
    └── updateNetwork(networkId, data)
```

## CSS Organization

```
Styles/
├── Auth.css
│   ├── .auth-container (full-page flex layout)
│   ├── .auth-card (white box with shadow)
│   ├── .form-group (input styling)
│   ├── .error-message (error styling)
│   └── button styling
│
└── Dashboard.css
    ├── .dashboard-container (main layout)
    ├── .dashboard-header (gradient header)
    ├── .dashboard-content (content area)
    ├── .section (white card)
    ├── .tickets-list (grid layout)
    ├── .ticket-card (individual ticket)
    ├── .status (status badges)
    ├── .tabs (tab navigation)
    ├── .assign-form (assignment form)
    ├── .reports-grid (report cards)
    └── Responsive media queries
```

## Request/Response Examples

### Register Request/Response
```
POST /auth/register
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "customer"
}

Response:
{
  "id": "507f1f77bcf86cd799439011",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "customer",
  "is_active": true
}
```

### Create Ticket Request/Response
```
POST /tickets
{
  "issue_type": "Network Down",
  "description": "Internet connection is not working",
  "location": "Office Building A"
}

Response:
{
  "id": "507f1f77bcf86cd799439012",
  "user_id": "507f1f77bcf86cd799439011",
  "issue_type": "Network Down",
  "description": "Internet connection is not working",
  "location": "Office Building A",
  "status": "open",
  "created_at": "2024-03-31T10:30:00Z"
}
```

## Error Handling Flow

```
API Call
    │
    ├─ Success ──┐
    │            └─ Return data
    │               Update state
    │               Re-render UI
    │
    └─ Error ────┐
               ├─ Extract error message
               ├─ Set error state
               ├─ Display error to user
               └─ Log to console
```

## Performance Optimizations

1. **Lazy loading** - Components only fetch data when needed
2. **Conditional rendering** - Don't render hidden tabs/sections
3. **Efficient state updates** - Use React hooks properly
4. **API caching** - Store tickets in state, don't re-fetch unnecessarily
5. **Responsive images** - None currently, but ready for future
6. **CSS optimization** - Separate files by feature

## Security Features

1. **JWT Authentication** - Tokens stored in localStorage
2. **Protected Routes** - ProtectedRoute wrapper
3. **Token Injection** - Automatic in all requests via axios interceptor
4. **Route Guards** - Check authentication before rendering
5. **Logout Clears** - Removes token and user data
6. **HTTPS Ready** - Works with/without HTTPS

## Browser Support

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Responsive design

## Development Tools

- **Vite** - Fast dev server, instant HMR
- **React DevTools** - Debug component state
- **Redux DevTools** - (not used, but context available)
- **Axios DevTools** - Monitor API calls
- **Browser DevTools** - Network, Console, Elements tabs
