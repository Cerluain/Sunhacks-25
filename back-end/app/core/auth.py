# --- Imports ---
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas.user import TokenData

# --- Password Hashing Setup ---
# Create a CryptContext instance for hashing passwords.
# We specify "bcrypt" as the hashing scheme.
# "deprecated="auto"" means it will automatically handle upgrading hashes if needed in the future.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Password Utility Functions ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that a plain-text password matches a hashed password.

    Args:
        plain_password (str): The plain-text password to check.
        hashed_password (str): The stored hashed password.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password using the configured hashing algorithm.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The resulting hashed password.
    """
    return pwd_context.hash(password)

# --- JWT Token Functions ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token.

    Args:
        data (dict): The data (payload) to include in the token (e.g., user ID).
        expires_delta (Optional[timedelta]): The lifespan of the token. If not provided,
                                             it defaults to the value from settings.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    
    # Determine the token's expiration time.
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Use the default expiration time from settings if none is provided.
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add the expiration time to the payload.
    to_encode.update({"exp": expire})
    
    # Encode the payload into a JWT string.
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET, 
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_token(token: str) -> TokenData:
    """
    Decodes a JWT access token and validates its payload.

    Args:
        token (str): The JWT token to decode.

    Raises:
        JWTError: If the token is invalid, expired, or has a bad signature.

    Returns:
        TokenData: The validated token data containing the user identifier.
    """
    try:
        # Attempt to decode the token using the secret key and algorithm from settings.
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        
        # The 'sub' (subject) claim is expected to hold the user's unique identifier.
        user_id: str = payload.get("sub")
        
        if user_id is None:
            # If the 'sub' claim is missing, the token is invalid.
            raise JWTError("Subject claim ('sub') missing from token.")
            
        return TokenData(sub=user_id)
        
    except JWTError as e:
        # Re-raise the exception to be handled by the dependency layer.
        # This keeps the core auth logic clean of HTTP-specific error handling.
        raise e
