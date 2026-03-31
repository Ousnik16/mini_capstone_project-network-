# 🚀 Quick Start Guide

## In 3 Steps:

### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

### Step 2: Start Frontend
```bash
npm run dev
```

### Step 3: Start Backend (in another terminal)
```bash
python -m uvicorn app.main:app --reload
```

## You're Ready! 🎉

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

## Default Test Accounts

### Create Your Test Accounts:
1. Go to http://localhost:5173/register
2. Choose role: **Customer**, **Engineer**, or **Admin**
3. Register and start testing!

## What Can You Do?

### 👥 As Customer:
- Create support tickets
- View your tickets
- Track status

### 👨‍💼 As Engineer:
- View assigned tickets
- Mark tickets as resolved

### 👨‍💻 As Admin:
- View all tickets
- Assign tickets to engineers
- View reports & analytics
- Manage network nodes

## Features Overview

✅ **Authentication** - Secure login/register with roles
✅ **Ticket Management** - Full CRUD operations
✅ **Assignment System** - Admins assign work to engineers
✅ **Reports** - System analytics and metrics
✅ **Network Management** - Infrastructure management
✅ **Responsive Design** - Works on all devices
✅ **Protected Routes** - Role-based access control

## Troubleshooting

**Frontend won't load?**
- Make sure `npm install` completed
- Check VITE_API_BASE_URL in `.env`

**Can't login?**
- Ensure backend is running
- Check backend is on port 8000

**See blank page?**
- Press F12 to open DevTools
- Check Console for errors

## File Locations

- Frontend Code: `frontend/src/`
- Styles: `frontend/src/styles/`
- API Client: `frontend/src/services/api.js`
- Pages: `frontend/src/pages/`
- Auth Context: `frontend/src/contexts/AuthContext.jsx`

## Next Steps

1. ✅ Install dependencies
2. ✅ Start both servers
3. ✅ Register as different roles
4. ✅ Test all features
5. ✅ Check backend logs for errors

Enjoy! 🎊

---
For detailed information, see `FRONTEND_SETUP.md` or `FRONTEND_IMPLEMENTATION_SUMMARY.md`
