# --- Imports ---
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

# Import project-specific modules
from ..dependencies import get_db
from app.crud import crud_user
from app.schemas.user import User, UserCreate
from ..dependencies import get_current_active_user


# --- Router Initialization ---
# Create a new APIRouter instance for user-related endpoints.
router = APIRouter(prefix="/users", tags=["users"])


# --- API Endpoints ---

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
):
    """
    Create a new user.

    This endpoint handles user registration. It takes user details,
    checks if a user with the same email already exists, and if not,

    creates a new user in the database.
    """
    # Check if a user with the given email already exists in the database.
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        # If a user exists, raise an HTTP 400 Bad Request error.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )
    
    # If the email is unique, create the new user.
    user = crud_user.create(db, obj_in=user_in)
    
    # Return the newly created user object.
    # The `response_model=User` will filter out the hashed_password.
    return user


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get the current logged-in user's details.

    This is a protected endpoint that uses the `get_current_active_user`
    dependency to ensure only authenticated and active users can access it.
    It returns the data for the user associated with the provided JWT token.
    """
    return current_user
