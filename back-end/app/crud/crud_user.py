# --- Imports ---
from sqlalchemy.orm import Session
from typing import Optional, Any
import uuid

# Import project-specific modules
from app.core.auth import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

# --- CRUD Functions for User Model ---

def get(db: Session, id: uuid.UUID) -> Optional[User]:
    """
    Retrieve a single user from the database by their ID.

    Args:
        db (Session): The database session.
        id (uuid.UUID): The UUID of the user to retrieve.

    Returns:
        Optional[User]: The user object if found, otherwise None.
    """
    return db.query(User).filter(User.id == id).first()

def get_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieve a single user from the database by their email address.

    Args:
        db (Session): The database session.
        email (str): The email address of the user to retrieve.

    Returns:
        Optional[User]: The user object if found, otherwise None.
    """
    return db.query(User).filter(User.email == email).first()

def create(db: Session, obj_in: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        obj_in (UserCreate): The Pydantic schema containing the new user's data.

    Returns:
        User: The newly created user's SQLAlchemy model object.
    """
    # Hash the plain-text password before storing it.
    hashed_password = get_password_hash(obj_in.password)
    
    # Create a dictionary of the data to be saved, excluding the plain password.
    db_obj = User(
        email=obj_in.email,
        full_name=obj_in.full_name,
        hashed_password=hashed_password
    )
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.

    Args:
        db (Session): The database session.
        email (str): The user's email.
        password (str): The user's plain-text password.

    Returns:
        Optional[User]: The authenticated user object if credentials are valid, else None.
    """
    from app.core.auth import verify_password
    
    user = get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
