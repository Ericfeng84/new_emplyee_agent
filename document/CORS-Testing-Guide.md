# CORS Testing Guide

## 📋 Overview

This guide provides step-by-step instructions for testing the CORS (Cross-Origin Resource Sharing) configuration after implementing the fixes. The fixes enable the frontend (running on `http://localhost:5173`) to communicate with the backend API (running on `http://localhost:8001`).

## 🎯 Prerequisites

Before testing, ensure you have:

1. **Backend server running** on port 8001
2. **Frontend server running** on port 5173
3. **curl** installed (for command-line testing)
4. **Modern browser** (Chrome, Firefox, Safari, or Edge)

## 🚀 Quick Start

### 1. Start the Backend Server

```bash
# From the project root directory
python run_server.py
```

The server should start and display:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### 2. Start the Frontend Server

In a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Start the development server
npm run dev
```

The frontend should start and display:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## 🧪 Testing Methods

### Method 1: Automated Shell Script (Recommended)

The project includes an automated test script that verifies all CORS endpoints.

**Location:** [`test/test_cors_configuration.sh`](test/test_cors_configuration.sh:1)

**Usage:**

```bash
# Make the script executable (if not already)
chmod +x test/test_cors_configuration.sh

# Run the test script
./test/test_cors_configuration.sh
```

**What it tests:**
1. Health check endpoint (GET request)
2. OPTIONS preflight to `/v1/sessions/`
3. POST request to create a session
4. OPTIONS preflight to `/v1/chat/completions`
5. POST request to send a message

**Expected output:**
```
==========================================
CORS Configuration Test Script
==========================================

✓ Server is running

Test 1: Health Check (GET request)
----------------------------------------
Response Code: 200
Response Body: {"status": "ok", "version": "0.5.0"}
✓ PASS: Health check successful

Test 2: OPTIONS Preflight Request to /sessions/
----------------------------------------
Response Code: 200
✓ Access-Control-Allow-Origin header found
  Access-Control-Allow-Origin: http://localhost:5173
✓ Access-Control-Allow-Methods header found
  Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
✓ Access-Control-Allow-Headers header found
  Access-Control-Allow-Headers: Content-Type, Authorization, ...
✓ PASS: OPTIONS request successful

... (more tests)

==========================================
CORS Configuration Test Complete
==========================================

If all tests passed, CORS is configured correctly!
You can now test the frontend at: http://localhost:5173
```

### Method 2: Manual curl Commands

If you prefer to test manually, use these curl commands:

#### Test 1: Health Check

```bash
curl -X GET http://localhost:8001/v1/health
```

**Expected response:**
```json
{"status": "ok", "version": "0.5.0"}
```

#### Test 2: OPTIONS Preflight to Sessions

```bash
curl -X OPTIONS \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v http://localhost:8001/v1/sessions/
```

**Expected response:**
- HTTP 200 status code
- Headers include:
  - `Access-Control-Allow-Origin: http://localhost:5173`
  - `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`
  - `Access-Control-Allow-Headers: Content-Type, Authorization, ...`

#### Test 3: Create Session

```bash
curl -X POST \
  -H "Origin: http://localhost:5173" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}' \
  -v http://localhost:8001/v1/sessions/
```

**Expected response:**
- HTTP 200 status code
- JSON body: `{"session_id": "..."}`
- Header: `Access-Control-Allow-Origin: http://localhost:5173`

#### Test 4: OPTIONS Preflight to Chat

```bash
curl -X OPTIONS \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v http://localhost:8001/v1/chat/completions
```

**Expected response:**
- HTTP 200 status code
- CORS headers present

#### Test 5: Send Message

```bash
curl -X POST \
  -H "Origin: http://localhost:5173" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello"}],
    "session_id": "test_session_123",
    "user": "test_user"
  }' \
  -v http://localhost:8001/v1/chat/completions
```

**Expected response:**
- HTTP 200 status code (or 500 if agent not fully configured)
- CORS headers present

### Method 3: Browser Testing

#### Step 1: Open Browser DevTools

1. Open your browser
2. Navigate to `http://localhost:5173`
3. Open Developer Tools (F12 or Cmd+Option+I)
4. Go to the **Console** tab

#### Step 2: Test API Calls

In the browser console, run these JavaScript commands:

```javascript
// Test 1: Health check
fetch('http://localhost:8001/v1/health')
  .then(r => r.json())
  .then(d => console.log('Health check:', d))
  .catch(e => console.error('Health check failed:', e));

// Test 2: Create session
fetch('http://localhost:8001/v1/sessions/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ user_id: 'test_user' })
})
  .then(r => r.json())
  .then(d => console.log('Session created:', d))
  .catch(e => console.error('Session creation failed:', e));

// Test 3: Send message
fetch('http://localhost:8001/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    messages: [{ role: 'user', content: 'Hello' }],
    session_id: 'test_session_123',
    user: 'test_user'
  })
})
  .then(r => r.json())
  .then(d => console.log('Chat response:', d))
  .catch(e => console.error('Chat failed:', e));
```

#### Step 3: Check Network Tab

1. Switch to the **Network** tab in DevTools
2. Filter by "Fetch/XHR"
3. Look for the requests you just made
4. Click on each request and check:
   - **Status Code**: Should be 200 (or 500 for chat if agent not configured)
   - **Response Headers**: Should include CORS headers
   - **Console**: Should show no CORS errors

#### Step 4: Test Frontend UI

1. Use the chat interface at `http://localhost:5173`
2. Type a message and send it
3. Check the Console for any errors
4. Check the Network tab for the request/response

## 🔍 Troubleshooting

### Issue 1: "Server is not running"

**Solution:**
```bash
# Start the backend server
python run_server.py
```

### Issue 2: CORS errors in browser console

**Symptoms:**
- Error: "Access to XMLHttpRequest at 'http://localhost:8001/v1/sessions/' from origin 'http://localhost:5173' has been blocked by CORS policy"

**Possible causes:**
1. Backend server not restarted after CORS changes
2. Browser caching old CORS responses
3. Multiple CORS middleware layers

**Solutions:**
1. **Restart the backend server:**
   ```bash
   # Stop the server (Ctrl+C)
   # Start it again
   python run_server.py
   ```

2. **Clear browser cache:**
   - Open DevTools (F12)
   - Right-click the refresh button
   - Select "Empty Cache and Hard Reload"
   - Or use incognito/private mode

3. **Check for duplicate middleware:**
   - Review [`nexus_agent/api/main.py`](nexus_agent/api/main.py:1)
   - Ensure CORS middleware is added only once

### Issue 3: OPTIONS request returns 405 Method Not Allowed

**Symptoms:**
- OPTIONS requests fail with 405 status
- Preflight requests not being handled

**Solutions:**
1. Check that the OPTIONS handler is present in [`main.py`](nexus_agent/api/main.py:76-88)
2. Verify CORS middleware is added BEFORE routers
3. Restart the backend server

### Issue 4: Credentials not working

**Symptoms:**
- Requests fail when `withCredentials: true` is set
- CORS errors related to credentials

**Solutions:**
1. Check that `allow_credentials=True` is set in CORS middleware
2. Ensure specific origins are used instead of `*` when credentials are enabled
3. Verify frontend axios has `withCredentials: true`

### Issue 5: Frontend shows "Failed to get response from agent"

**Symptoms:**
- Frontend can create sessions but fails to send messages
- Error: "Failed to get response from agent. Please try again."

**Possible causes:**
1. Agent not properly configured
2. Missing environment variables
3. Redis not running (if memory is enabled)

**Solutions:**
1. Check backend logs for errors
2. Verify `.env` file has required API keys
3. Ensure Redis is running if using memory management
4. Check [`nexus_agent/config/settings.py`](nexus_agent/config/settings.py:1) for configuration

## 📊 Expected Results

After successful CORS configuration, you should see:

### Backend Logs
```
INFO: CORS request from origin: http://localhost:5173, method: OPTIONS
INFO: OPTIONS request received for path: /v1/sessions/
INFO: CORS request from origin: http://localhost:5173, method: POST
```

### Browser Console
```
[API] POST /sessions/ {user_id: "demo_user"}
[API] Response 200: {session_id: "..."}
[API] POST /chat/completions {messages: Array(1), session_id: "...", user: "demo_user"}
[API] Response 200: {id: "...", choices: Array(1), ...}
```

### Browser Network Tab
- All requests show status 200 (or 500 for chat if agent not configured)
- Response headers include CORS headers
- No CORS errors in console

## ✅ Verification Checklist

Use this checklist to verify CORS is working correctly:

- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Automated test script passes all tests
- [ ] OPTIONS requests return 200 status
- [ ] POST requests return 200 status
- [ ] CORS headers are present in responses
- [ ] Frontend can create sessions
- [ ] Frontend can send messages
- [ ] Frontend receives responses
- [ ] No CORS errors in browser console
- [ ] Backend logs show CORS requests

## 📚 Additional Resources

- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Axios CORS Configuration](https://github.com/axios/axios#config-defaults)

## 🎉 Success Criteria

CORS is successfully configured when:

1. ✅ All automated tests pass
2. ✅ Frontend can create sessions without errors
3. ✅ Frontend can send messages without errors
4. ✅ Frontend receives responses from the backend
5. ✅ No CORS errors appear in browser console
6. ✅ Backend logs show CORS requests being handled

## 📞 Support

If you encounter issues not covered in this guide:

1. Check the backend logs for error messages
2. Review the CORS configuration in [`nexus_agent/api/main.py`](nexus_agent/api/main.py:1)
3. Verify the frontend API client in [`frontend/src/api/client.js`](frontend/src/api/client.js:1)
4. Consult the detailed CORS fix plan at [`plans/cors-fix-plan.md`](plans/cors-fix-plan.md:1)
