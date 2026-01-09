# Quick Start Guide

## Prerequisites

Before starting, ensure you have the following installed:

- Python 3.9+
- Node.js 18+
- Redis server
- UV package manager

## Starting the Development Environment

### Option 1: Using the Startup Script (Recommended)

```bash
# Start Redis and backend server
./start_dev.sh

# In another terminal, start the frontend
cd frontend
npm run dev
```

### Option 2: Manual Startup

```bash
# Terminal 1: Start Redis
redis-server --daemonize yes

# Terminal 2: Start backend server
python run_server.py

# Terminal 3: Start frontend
cd frontend
npm run dev
```

## Access Points

Once all services are running:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **Redis**: localhost:6379

## Common Issues and Solutions

### Issue: "Network Error" in Frontend

**Solution**: Check if Redis is running
```bash
lsof -i :6379
```

If Redis is not running:
```bash
redis-server --daemonize yes
```

### Issue: "Connection Refused" on Port 8001

**Solution**: Check if backend is running
```bash
lsof -i :8001
```

If backend is not running:
```bash
python run_server.py
```

### Issue: CORS Errors

**Solution**: The CORS configuration is already set up correctly. If you see CORS errors, it's likely because:
1. Redis is not running (causing 500 errors)
2. Backend is not running
3. Wrong port configured in frontend

Verify services are running:
```bash
# Check Redis
redis-cli ping  # Should return PONG

# Check Backend
curl http://localhost:8001/v1/health  # Should return {"status":"ok","version":"0.5.0"}
```

## Stopping Services

### Stop Backend
```bash
# If using the startup script
kill $(cat .backend_pid) 2>/dev/null

# Or find and kill the process
kill $(lsof -t -i:8001)
```

### Stop Redis
```bash
redis-cli shutdown
```

### Stop Frontend
Press `Ctrl+C` in the terminal where it's running.

## Testing the Setup

### Test Backend Health
```bash
curl http://localhost:8001/v1/health
```

### Test Session Creation
```bash
curl -X POST http://localhost:8001/v1/sessions/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "demo_user"}'
```

### Test Chat Completion
```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello"}],
    "session_id": "test-session",
    "user": "demo_user"
  }'
```

## Development Workflow

1. **Start services** (using startup script or manually)
2. **Open browser** to http://localhost:5173
3. **Test the chat interface** by sending a message
4. **Check browser console** for any errors (F12 → Console tab)
5. **Check Network tab** for API calls (F12 → Network tab)

## Useful Commands

### Check what's running on ports
```bash
# Backend
lsof -i :8001

# Frontend
lsof -i :5173

# Redis
lsof -i :6379
```

### View Redis data
```bash
redis-cli
> KEYS *
> GET <key_name>
> EXIT
```

### View backend logs
If using the startup script, logs are shown in the terminal. Otherwise, check the terminal where you ran `python run_server.py`.

### Test API with CORS headers
```bash
curl -v -X POST http://localhost:8001/v1/sessions/ \
  -H "Origin: http://localhost:5173" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "demo_user"}'
```

Look for these headers in the response:
- `access-control-allow-origin: http://localhost:5173`
- `access-control-allow-credentials: true`

## Project Structure

```
new_emplyee_agent/
├── nexus_agent/           # Backend Python code
│   ├── api/              # FastAPI routes and middleware
│   ├── agent/            # LangChain agent implementation
│   ├── storage/          # Redis session management
│   ├── rag/              # Document retrieval
│   └── config/           # Configuration settings
├── frontend/             # React frontend
│   ├── src/
│   │   ├── api/          # API client (client.js)
│   │   ├── components/   # React components
│   │   └── App.jsx       # Main app component
├── document/             # Documentation
├── test/                 # Test files
├── start_dev.sh          # Startup script
└── run_server.py         # Backend server entry point
```

## Next Steps

1. ✅ Start Redis and backend server
2. ✅ Start the frontend
3. ✅ Test the chat interface
4. 📖 Read the [CORS Issue Resolution](CORS-Issue-Resolution.md) for detailed troubleshooting
5. 📖 Check the [API Documentation](http://localhost:8001/docs) for available endpoints

## Getting Help

If you encounter issues:

1. Check the [CORS Issue Resolution](CORS-Issue-Resolution.md) document
2. Review the server logs in your terminal
3. Check browser console for frontend errors
4. Verify all services are running using the commands above

---

**Last Updated**: 2026-01-09
