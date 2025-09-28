# --- Imports ---
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

# Import project-specific modules
from app.db.session import SessionLocal
from app.core import auth as auth_core
from app.core.config import settings
from app.crud import crud_user
from app.schemas.user import TokenData
from app.models.user import User

# --- Database Dependency ---
def get_db():
    """
    FastAPI dependency that creates and yields a new database session for each request.
    Ensures the session is always closed, even if errors occur.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Security Scheme ---
# Defines the security scheme (Bearer Tokens) and specifies the URL where a client
# can post a username and password to get a token. FastAPI uses this for documentation
# and to correctly parse the "Authorization: Bearer <token>" header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# --- Authentication Dependencies ---
async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency to get the current user from a JWT token.

    - Decodes the JWT token from the Authorization header.
    - Validates the token's payload to get the user ID ('sub').
    - Fetches the user from the database.
    - Raises HTTPException 401 if the token is invalid or the user doesn't exist.

    Args:
        db (Session): The database session dependency.
        token (str): The OAuth2 bearer token extracted from the request header.

    Returns:
        User: The authenticated user's SQLAlchemy model object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token using the secret key and algorithm from settings.
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        # The payload should contain the user ID in the 'sub' (subject) field.
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # Use a Pydantic model for data validation of the token's payload.
        token_data = TokenData(sub=user_id)
    except JWTError:
        # If decoding fails (e.g., invalid signature, expired token), raise the exception.
        raise credentials_exception
    
    # Fetch the user from the database using the ID from the token.
    user = crud_user.get(db, id=token_data.sub)
    if user is None:
        # If no user is found with that ID, the token is invalid.
        raise credentials_exception
    
    # Return the user object, making it available to the endpoint.
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to get the current *active* user.

    - First, it depends on `get_current_user` to authenticate the user.
    - Then, it checks if the authenticated user's `is_active` flag is True.
    - This is useful for disabling or banning users without deleting their accounts.

    Args:
        current_user (User): The user object from the `get_current_user` dependency.

    Raises:
        HTTPException: 403 Forbidden if the user is marked as inactive.

    Returns:
        User: The authenticated and active user's SQLAlchemy model object.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user
