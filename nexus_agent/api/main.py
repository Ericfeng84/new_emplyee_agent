from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from nexus_agent.api.routers import chat, health, sessions
from nexus_agent.config.settings import config
from nexus_agent.utils.logger import get_logger

logger = get_logger(__name__)

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    This function sets up the FastAPI app with:
    - CORS middleware for cross-origin requests
    - API routers for health, chat, and sessions endpoints
    - OPTIONS handler for preflight requests
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title="Nexus Agent API",
        description="Enterprise Agent Service",
        version="0.5.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Configure CORS with explicit settings
    # This allows the frontend (localhost:5173) to communicate with the backend (localhost:8001)
    app.add_middleware(
        CORSMiddleware,
        # Allow specific origins instead of wildcard for better security
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",  # Common development port
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,  # Required for cookies/auth headers
        allow_methods=[
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "OPTIONS",  # Explicitly include OPTIONS for preflight
        ],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "Accept",
            "Origin",
            "Access-Control-Request-Method",
            "Access-Control-Request-Headers",
        ],
        expose_headers=[
            "Content-Length",
            "Content-Type",
        ],
        max_age=600,  # Cache preflight response for 10 minutes
    )
    
    # Add CORS logging middleware for debugging
    @app.middleware("http")
    async def log_cors_requests(request: Request, call_next):
        """
        Log CORS-related requests for debugging purposes.
        
        This middleware logs the origin and method of incoming requests
        to help diagnose CORS issues during development.
        """
        origin = request.headers.get("origin")
        if origin:
            logger.info(f"CORS request from origin: {origin}, method: {request.method}")
        response = await call_next(request)
        return response
    
    # Add explicit OPTIONS handler for preflight requests
    # This ensures that all OPTIONS requests are properly handled
    @app.options("/{path:path}")
    async def options_handler(path: str):
        """
        Handle OPTIONS preflight requests explicitly.
        
        Browser sends OPTIONS requests before actual requests to check CORS policy.
        This handler ensures all paths respond correctly to preflight checks.
        
        Args:
            path: The URL path that was requested
            
        Returns:
            dict: Success response indicating OPTIONS request was handled
        """
        logger.info(f"OPTIONS request received for path: {path}")
        return {"status": "ok", "message": "CORS preflight successful"}
    
    # Register Routers
    # Note: Routers are registered AFTER CORS middleware to ensure CORS applies to all routes
    app.include_router(health.router, prefix="/v1", tags=["Health"])
    app.include_router(chat.router, prefix="/v1/chat", tags=["Chat"])
    app.include_router(sessions.router, prefix="/v1/sessions", tags=["Sessions"])
    
    return app

# Create the application instance
app = create_app()
