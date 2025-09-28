from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from app.routes import api_router

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
            "/api/auth/register"
        }
    
    async def dispatch(self, request: Request, call_next):
        # Check if the endpoint is public
        if request.url.path in self.public_endpoints:
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

# Add authentication middleware
app.add_middleware(AuthenticationMiddleware)

# Include all routes with a common prefix
app.include_router(api_router, prefix="/api")

