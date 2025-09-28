# --- Imports ---
import uuid
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# --- Token Schemas ---

class Token(BaseModel):
    """
    Schema for the JWT access token response. This is what the client
    receives upon successful login.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for the data contained within the JWT token.
    'sub' is the standard JWT claim for the subject (in our case, the user ID).
    """
    sub: str

# --- User Schemas ---

# Base properties shared across multiple user-related schemas.
class UserBase(BaseModel):
    """
    Base schema for user properties. Includes fields that are common
    for both user creation and user reading.
    """
    email: EmailStr  # Pydantic validates this is a valid email format.
    full_name: Optional[str] = None

# Properties required for creating a new user.
class UserCreate(UserBase):
    """
    Schema for creating a new user. Inherits from UserBase and adds the password field.
    This schema is used as the request body for the user creation endpoint.
    """
    password: str

# Properties required for updating an existing user.
class UserUpdate(UserBase):
    """
    Schema for updating a user. All fields are optional, so clients
    can update only the fields they need to.
    """
    password: Optional[str] = None

# Properties that are present in the database model but should be exposed via the API.
class User(UserBase):
    """

    Schema for reading/returning a user from the API.
    It inherits from UserBase and adds fields that should be public.
    Crucially, it does NOT include the `hashed_password`.
    """
    id: uuid.UUID
    is_active: bool
    
    # This configuration tells Pydantic to read the data even if it is not a dict,
    # but an ORM model (or any other arbitrary object with attributes).
    # This is necessary to map SQLAlchemy model instances to Pydantic schemas.
    model_config = ConfigDict(from_attributes=True)
