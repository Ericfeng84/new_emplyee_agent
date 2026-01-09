# CORS Fix Plan - Sprint 5

## 🎯 Problem Statement

The frontend (running on `http://localhost:5173`) cannot communicate with the backend API (running on `http://localhost:8001`) due to CORS policy blocking. Specifically:

- POST requests to `http://localhost:8001/v1/sessions/` are blocked
- Error: "Access to XMLHttpRequest at 'http://localhost:8001/v1/sessions/' from origin 'http://localhost:5173' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource."
- GET requests to `/v1/health` work correctly (returns 200)

## 🔍 Root Cause Analysis

### Current Configuration Issues

1. **CORS Middleware Applied but Not Working**
   - Location: [`nexus_agent/api/main.py`](nexus_agent/api/main.py:16-26)
   - The CORS middleware is configured with correct settings
   - However, the middleware might not be handling preflight OPTIONS requests correctly

2. **Preflight Request Handling**
   - Browser sends OPTIONS request before POST requests
   - FastAPI's CORSMiddleware should handle this automatically
   - The error suggests OPTIONS requests are not being processed

3. **Trailing Slash Issue**
   - Frontend calls: `/sessions/` (with trailing slash)
   - Router definition: `@router.post("/")` (matches with trailing slash)
   - This should work, but might be causing issues with CORS

4. **Middleware Order**
   - CORS middleware must be added BEFORE routers
   - Current order appears correct, but needs verification

## 📋 Proposed Solutions

### Solution 1: Enhanced CORS Configuration (Primary Fix)

**File:** [`nexus_agent/api/main.py`](nexus_agent/api/main.py)

#### Changes Required:

1. **Update CORS Middleware Configuration**
   ```python
   # Configure CORS with explicit settings
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:5173",
           "http://127.0.0.1:5173",
           "http://localhost:3000",  # Common dev port
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
       max_age=600,  # Cache preflight response for 10 minutes
   )
   ```

2. **Add Explicit OPTIONS Handler**
   ```python
   @app.options("/{path:path}")
   async def options_handler(path: str):
       """Handle OPTIONS preflight requests explicitly"""
       return {"status": "ok"}
   ```

### Solution 2: Router Path Standardization

**File:** [`nexus_agent/api/routers/sessions.py`](nexus_agent/api/routers/sessions.py)

#### Changes Required:

1. **Add Explicit OPTIONS Handlers for Each Route**
   ```python
   @router.post("/", response_model=Dict[str, str])
   @router.options("/", response_model=Dict[str, str])
   async def create_session(
       user_id: Optional[str] = Body(None, embed=True),
       agent: NexusLangChainAgent = Depends(get_nexus_agent)
   ):
       # ... existing code
   ```

2. **Add CORS Headers to Responses**
   ```python
   from fastapi import Response
   
   @router.post("/", response_model=Dict[str, str])
   async def create_session(
       user_id: Optional[str] = Body(None, embed=True),
       agent: NexusLangChainAgent = Depends(get_nexus_agent),
       response: Response = None
   ):
       # ... existing code
       response.headers["Access-Control-Allow-Origin"] = "*"
       return {"session_id": session_id}
   ```

### Solution 3: Frontend Fallback (Backup)

**File:** [`frontend/src/api/client.js`](frontend/src/api/client.js)

#### Changes Required:

1. **Add CORS Mode to Axios Configuration**
   ```javascript
   const client = axios.create({
       baseURL: API_BASE_URL,
       headers: {
           'Content-Type': 'application/json',
       },
       withCredentials: true,  // Enable CORS credentials
   });
   ```

2. **Add Error Handling for CORS Issues**
   ```javascript
   createSession: async (userId = 'demo_user') => {
       try {
           const response = await client.post('/sessions/', {
               user_id: userId
           });
           return response.data;
       } catch (error) {
           if (error.response?.status === 405) {
               console.error('Method not allowed - CORS issue');
           }
           throw error;
       }
   },
   ```

## 🛠️ Implementation Steps

### Step 1: Update Backend CORS Configuration
- [ ] Modify [`nexus_agent/api/main.py`](nexus_agent/api/main.py) with enhanced CORS settings
- [ ] Add explicit OPTIONS handler
- [ ] Restart the backend server

### Step 2: Test with curl
- [ ] Test OPTIONS request: `curl -X OPTIONS http://localhost:8001/v1/sessions/ -H "Origin: http://localhost:5173" -v`
- [ ] Test POST request: `curl -X POST http://localhost:8001/v1/sessions/ -H "Origin: http://localhost:5173" -H "Content-Type: application/json" -d '{"user_id": "test"}' -v`
- [ ] Verify CORS headers are present in responses

### Step 3: Test with Browser
- [ ] Open browser DevTools Console
- [ ] Navigate to `http://localhost:5173`
- [ ] Send a message through the chat interface
- [ ] Check Network tab for CORS headers
- [ ] Verify no CORS errors in Console

### Step 4: Verify All Endpoints
- [ ] Test `/v1/health` (GET)
- [ ] Test `/v1/sessions/` (POST)
- [ ] Test `/v1/sessions/{id}` (GET)
- [ ] Test `/v1/sessions/{id}/history` (GET)
- [ ] Test `/v1/chat/completions` (POST)

## 📊 Expected Results

After implementing the fixes:

1. **Preflight OPTIONS Requests** should return:
   ```
   Access-Control-Allow-Origin: http://localhost:5173
   Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
   Access-Control-Allow-Headers: Content-Type, Authorization, ...
   Access-Control-Max-Age: 600
   ```

2. **Actual POST Requests** should return:
   ```
   Access-Control-Allow-Origin: http://localhost:5173
   Content-Type: application/json
   ```

3. **Frontend** should successfully:
   - Create sessions
   - Send messages
   - Receive responses
   - No CORS errors in browser console

## 🔧 Troubleshooting Guide

### Issue 1: CORS Still Blocking After Fix
**Possible Causes:**
- Server not restarted after changes
- Browser caching old CORS responses
- Multiple CORS middleware layers

**Solutions:**
- Restart backend server: `python run_server.py`
- Clear browser cache or use incognito mode
- Check for duplicate middleware in code

### Issue 2: OPTIONS Request Returns 405 Method Not Allowed
**Possible Causes:**
- Router doesn't support OPTIONS method
- Middleware order is incorrect

**Solutions:**
- Add explicit OPTIONS handler to main.py
- Ensure CORS middleware is added before routers

### Issue 3: Credentials Not Working
**Possible Causes:**
- `allow_credentials=True` but origin is `*`
- Frontend not sending credentials

**Solutions:**
- Use specific origins instead of `*` when credentials are enabled
- Set `withCredentials: true` in axios

## 📝 Additional Recommendations

1. **Environment-Specific CORS Configuration**
   - Development: Allow all localhost ports
   - Production: Use specific domains only

2. **Add CORS Logging Middleware**
   ```python
   @app.middleware("http")
   async def log_cors(request: Request, call_next):
       origin = request.headers.get("origin")
       if origin:
           logger.info(f"CORS request from origin: {origin}")
       response = await call_next(request)
       return response
   ```

3. **Consider Using FastAPI-CORS Extension**
   - Alternative: `fastapi-cors` package for more advanced features
   - Provides rate limiting and additional security features

## ✅ Verification Checklist

After implementing the fixes, verify:

- [ ] Backend server starts without errors
- [ ] OPTIONS requests return correct CORS headers
- [ ] POST requests to `/v1/sessions/` succeed
- [ ] Frontend can create sessions
- [ ] Frontend can send messages
- [ ] Frontend receives responses without errors
- [ ] No CORS errors in browser console
- [ ] All API endpoints work correctly

## 📚 References

- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Axios CORS Configuration](https://github.com/axios/axios#config-defaults)
