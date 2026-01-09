# CORS Issue Resolution Summary

## Problem Description

The frontend (running on `http://localhost:5173`) was experiencing CORS errors when trying to connect to the backend API (running on `http://localhost:8001`). The errors included:

- `Access to XMLHttpRequest at 'http://localhost:8001/v1/sessions/' from origin 'http://localhost:5173' has been blocked by CORS policy`
- `Failed to load resource: net::ERR_CONNECTION_REFUSED`
- `Network Error - Check if backend is running`

## Root Cause Analysis

The issue was **NOT** a CORS configuration problem, but rather a **missing Redis server**. The CORS middleware in [`nexus_agent/api/main.py`](../nexus_agent/api/main.py:31) was correctly configured:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Accept",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["Content-Length", "Content-Type"],
    max_age=600,
)
```

### What Was Actually Happening

1. **CORS was working correctly** - The backend was properly returning CORS headers
2. **Redis was not running** - The session manager depends on Redis for storing session data
3. **500 Internal Server Error** - When the frontend tried to create a session, the backend failed because Redis was unavailable
4. **Network Error** - The frontend interpreted the 500 error as a network/CORS issue

## Solution

### Step 1: Start Redis Server

```bash
redis-server --daemonize yes
```

This starts Redis in the background as a daemon process.

### Step 2: Verify Redis is Running

```bash
lsof -i :6379
```

Expected output should show Redis listening on port 6379.

### Step 3: Restart the Backend Server (if needed)

The backend server was already running on port 8001. If you need to restart it:

```bash
python run_server.py
```

Or using uvicorn directly:

```bash
uvicorn nexus_agent.api.main:app --host 0.0.0.0 --port 8001 --reload
```

## Verification

### Test Backend Health

```bash
curl http://localhost:8001/v1/health
```

Expected response:
```json
{"status":"ok","version":"0.5.0"}
```

### Test Session Creation with CORS

```bash
curl -X POST http://localhost:8001/v1/sessions/ \
  -H "Origin: http://localhost:5173" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "demo_user"}' \
  -v
```

Expected response should include CORS headers:
```
< access-control-allow-credentials: true
< access-control-expose-headers: Content-Length, Content-Type
< access-control-allow-origin: http://localhost:5173
```

### Test Chat Completions

```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello"}],
    "session_id": "test-session",
    "user": "demo_user"
  }'
```

Expected response should include a chat completion from the agent.

## Current System Status

✅ **Backend Server**: Running on `http://localhost:8001`  
✅ **Redis Server**: Running on port 6379  
✅ **Frontend Server**: Running on `http://localhost:5173`  
✅ **CORS Configuration**: Properly configured and working  
✅ **Session Management**: Functional with Redis backend  

## Architecture Overview

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   Frontend       │         │   Backend       │         │    Redis        │
│   (React)        │         │   (FastAPI)     │         │   (Session      │
│   :5173          │         │   :8001         │         │    Storage)     │
│                 │         │                 │         │   :6379         │
│  client.js      │────────▶│  main.py        │────────▶│                 │
│  (axios)        │ CORS    │  (CORSMiddleware│         │                 │
│                 │         │   configured)   │         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

## Key Files

- **Backend CORS Configuration**: [`nexus_agent/api/main.py`](../nexus_agent/api/main.py:31)
- **Frontend API Client**: [`frontend/src/api/client.js`](../frontend/src/api/client.js:14)
- **Session Router**: [`nexus_agent/api/routers/sessions.py`](../nexus_agent/api/routers/sessions.py:8)
- **Session Manager**: [`nexus_agent/storage/session_manager.py`](../nexus_agent/storage/session_manager.py)
- **Redis Client**: [`nexus_agent/storage/redis_client.py`](../nexus_agent/storage/redis_client.py)

## Best Practices for Development

### 1. Always Start Redis Before Running Backend

Add this to your development workflow:

```bash
# Start Redis
redis-server --daemonize yes

# Verify Redis is running
redis-cli ping  # Should return PONG

# Start backend
python run_server.py
```

### 2. Check Server Status Before Debugging CORS

Before assuming it's a CORS issue:

1. Check if backend is running: `lsof -i :8001`
2. Check if Redis is running: `lsof -i :6379`
3. Test backend health: `curl http://localhost:8001/v1/health`
4. Test with curl first to isolate frontend issues

### 3. Monitor Backend Logs

The backend includes CORS logging middleware. Watch for these log messages:

```
INFO: CORS request from origin: http://localhost:5173, method: POST
INFO: OPTIONS request received for path: /v1/sessions/
```

### 4. Use Browser DevTools

When debugging frontend issues:

1. Open Browser DevTools (F12)
2. Go to Network tab
3. Filter by "XHR" or "Fetch"
4. Look for failed requests
5. Check the Response tab for error details
6. Check the Headers tab for CORS headers

## Troubleshooting Guide

### Issue: "Network Error" in Frontend

**Possible Causes:**
1. Backend server not running
2. Redis server not running
3. Wrong port configured
4. Firewall blocking connection

**Solutions:**
```bash
# Check backend
lsof -i :8001

# Check Redis
lsof -i :6379

# Test connection
curl http://localhost:8001/v1/health
```

### Issue: "CORS policy blocked" Error

**Possible Causes:**
1. Origin not in allowed origins list
2. Missing CORS headers in response
3. Credentials not allowed but required

**Solutions:**
1. Verify origin is in [`main.py`](../nexus_agent/api/main.py:34) allow_origins list
2. Check CORS headers in response: `curl -v -H "Origin: http://localhost:5173" http://localhost:8001/v1/health`
3. Ensure `allow_credentials=True` if using cookies/auth

### Issue: "500 Internal Server Error" on Session Creation

**Possible Causes:**
1. Redis not running
2. Redis connection issues
3. Session manager misconfiguration

**Solutions:**
```bash
# Check Redis status
redis-cli ping

# Check Redis logs
tail -f /usr/local/var/log/redis.log

# Test Redis connection
python -c "from nexus_agent.storage.redis_client import get_redis_client; print(get_redis_client().ping())"
```

## Next Steps

The CORS issue has been resolved. The frontend should now be able to:

1. ✅ Create sessions via `POST /v1/sessions/`
2. ✅ Send messages via `POST /v1/chat/completions`
3. ✅ Retrieve session history via `GET /v1/sessions/{session_id}/history`

To verify everything is working:

1. Open your browser to `http://localhost:5173`
2. Try sending a message in the chat interface
3. Check the browser console for any errors
4. Check the Network tab for successful API calls

## Additional Resources

- [CORS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [FastAPI CORS Middleware](https://fastapi.tiangolo.com/tutorial/cors/)
- [Redis Documentation](https://redis.io/documentation)
- [Project README](../README.md)

---

**Date**: 2026-01-09  
**Status**: ✅ Resolved  
**Verified**: Backend and frontend are communicating successfully
