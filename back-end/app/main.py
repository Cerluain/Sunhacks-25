from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from app.routes import api_router
from app.routes.auth import token_blacklist  # Import the token blacklist
from app.db import main as init_db  # Import database initialization
import os
from pathlib import Path

SECRET_KEY = "LEOISGAY"
ALGORITHM = "HS256"

class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to check authentication for protected endpoints
    """
    
    def __init__(self, app):
        super().__init__(app)
        # Define public endpoints that don't require authentication
        self.public_endpoints = {
            "/",
            "/docs",
            "/openapi.json", 
            "/redoc",
            "/api/auth/login",
            "/api/auth/register",
            "/api/auth/admin-login"
        }
        # Add patterns for static files (React build files)
        self.public_patterns = [
            "/static/",
            "/manifest.json",
           
        ]
    
    async def dispatch(self, request: Request, call_next):
        # Check if the endpoint is public
        if request.url.path in self.public_endpoints:
            return await call_next(request)
        
        # Check if it's a static file request
        for pattern in self.public_patterns:
            if request.url.path.startswith(pattern):
                return await call_next(request)
        
        # Check for Authorization header
        authorization = request.headers.get("Authorization")
        
        if not authorization or not authorization.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authentication required"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Extract token
        token = authorization.split(" ")[1] if len(authorization.split(" ")) > 1 else None
        
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token format"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Validate token
        try:
            # Check if token is blacklisted
            if token in token_blacklist:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Token has been invalidated"},
                    headers={"WWW-Authenticate": "Bearer"}
                )
                
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            user_id = payload.get("user_id")
            
            if not email or not user_id:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid token payload"},
                    headers={"WWW-Authenticate": "Bearer"}
                )
            
            # Add user info to request state for use in endpoints
            request.state.user_email = email
            request.state.user_id = user_id
            
        except JWTError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or expired token"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Continue to the endpoint
        return await call_next(request)

app = FastAPI()

# Initialize database
init_db()

# Add authentication middleware
app.add_middleware(AuthenticationMiddleware)

# Include all routes with a common prefix
app.include_router(api_router, prefix="/api")

# Get the path to the React build directory
# Assuming the back-end and front-end are in the same parent directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
REACT_BUILD_DIR = BASE_DIR / "front-end" / "build"

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory=str(REACT_BUILD_DIR / "static")), name="static")


@app.get("/manifest.json")
async def get_manifest():
    return FileResponse(str(REACT_BUILD_DIR / "manifest.json"))

# Catch-all route to serve React app for client-side routing
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """
    Serve the React app for all routes not handled by API endpoints.
    This enables client-side routing to work properly.
    """
    # If the request is for the API, let it pass through (shouldn't reach here due to prefix)
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # For all other routes, serve the React index.html
    index_file = REACT_BUILD_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    else:
        raise HTTPException(status_code=404, detail="React app not found. Please run 'npm run build' in the front-end directory.")

