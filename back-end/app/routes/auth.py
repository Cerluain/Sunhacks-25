import hashlib, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated

from pydantic import BaseModel, Field
from app.db import authenticate, User, create_user
from jose import JWTError, jwt

router = APIRouter()

SECRET_KEY = "LEOISGAY"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="login")

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

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(email: str, user_id: int, expires_delta: datetime.timedelta):
    to_encode = {"sub": email, "user_id": user_id}
    expires = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
  
async def get_current_user(token: str = Depends(oauth2_bearer)):
  try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      email: str = payload.get("sub")
      user_id: int = payload.get("user_id")
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
  return {"email": email, "user_id": user_id}

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
    
    token = create_access_token(
        email=user[1],
        user_id=user[0],
        expires_delta=datetime.timedelta(hours=1)
    ) if user else None

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    return {"access_token": token, "token_type": "bearer"}

