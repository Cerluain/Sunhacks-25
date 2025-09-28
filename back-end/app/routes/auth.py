import hashlib, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated, Set

from pydantic import BaseModel, Field
from app.db import authenticate, User, create_user
from jose import JWTError, jwt

router = APIRouter()

SECRET_KEY = "LEOISGAY"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="login")

# Token blacklist to store invalidated tokens
# In production, use Redis or database for persistence
token_blacklist: Set[str] = set()

class Token(BaseModel):
    access_token: str
    token_type: str

class CreateUserRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=6, max_length=100)

class UserResponse(BaseModel):
    id: int
    email: str
    message: str

class LogoutResponse(BaseModel):
    message: str

def create_access_token(email: str, user_id: int, is_admin: bool = False, expires_delta: datetime.timedelta = None):
    to_encode = {"sub": email, "user_id": user_id, "is_admin": is_admin}
    if expires_delta:
        expires = datetime.datetime.utcnow() + expires_delta
    else:
        expires = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
  
async def get_current_user(token: str = Depends(oauth2_bearer)):
  try:
      # Check if token is blacklisted
      if token in token_blacklist:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Token has been invalidated",
              headers={"WWW-Authenticate": "Bearer"},
          )
      
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      email: str = payload.get("sub")
      user_id: int = payload.get("user_id")
      is_admin: bool = payload.get("is_admin", False)
      
      if email is None or user_id is None:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Could not validate credentials",
              headers={"WWW-Authenticate": "Bearer"},
          )
  except JWTError:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Could not validate credentials",
          headers={"WWW-Authenticate": "Bearer"},
      )
  return {"email": email, "user_id": user_id, "is_admin": is_admin}

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: CreateUserRequest):
    """
    Register a new user using email as username
    
    - **email**: Email address (must be unique and valid, used as username)
    - **password**: Password (6-100 characters, will be hashed)
    """
    # Hash the password
    password_hash = hashlib.sha256(user_data.password.encode()).hexdigest()
    
    # Create the user using email as both username and email
    new_user = create_user(
        username=user_data.email,  # Use email as username
        email=user_data.email, 
        password_hash=password_hash
    )
    
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        message="User created successfully"
    )

@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Hash the password before authentication
    password_hash = hashlib.sha256(form_data.password.encode()).hexdigest()
    
    # Use email as username - form_data.username will contain the email
    user = authenticate(form_data.username, password_hash)
    
    if user:
        token = create_access_token(
            email=user[1],
            user_id=user[0],
            is_admin=user[3],  # Admin status from database
            expires_delta=datetime.timedelta(hours=1)
        )
    else:
        token = None

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout", response_model=LogoutResponse)
async def logout(request: Request):
    """
    Logout user by invalidating their JWT token
    
    This endpoint adds the token to a blacklist, preventing its future use.
    The client should also remove the token from local storage.
    """
    # Get the token from the Authorization header
    authorization = request.headers.get("Authorization")
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No valid token provided",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = authorization.split(" ")[1] if len(authorization.split(" ")) > 1 else None
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Verify token is valid before blacklisting
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Add token to blacklist
    token_blacklist.add(token)
    
    return {"message": "Successfully logged out"}


@router.post("/admin-login", response_model=Token)
async def admin_login():
    """
    Automatic admin login for development/demo purposes
    
    Logs in with the default admin account (admin@gmail.com / admin123)
    Returns a JWT token with admin privileges.
    """
    admin_email = "admin@gmail.com"
    admin_password = "admin123"
    
    # Hash the password
    password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
    
    # Authenticate admin
    user = authenticate(admin_email, password_hash)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin account not found. Please ensure the database is initialized."
        )
    
    # Create admin token
    token = create_access_token(
        email=user[1],
        user_id=user[0],
        is_admin=user[3],
        expires_delta=datetime.timedelta(hours=24)  # Longer expiry for admin
    )
    
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user information
    
    Returns the email and user_id of the currently authenticated user.
    Requires valid JWT token.
    """
    return {
        "email": current_user["email"],
        "user_id": current_user["user_id"],
        "is_admin": current_user.get("is_admin", False),
        "message": "User information retrieved successfully"
    }

