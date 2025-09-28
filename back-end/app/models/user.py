# --- Imports ---
import uuid
from sqlalchemy import Boolean, Column, String

# Import the Base class from our custom base_class module
from app.db.base_class import Base

# --- User Model Definition ---
class User(Base):
    """
    SQLAlchemy model representing a user in the database.
    """
    # Define the table name in the database.
    __tablename__ = "users"

    # Define the table columns.
    
    # Primary Key: A universally unique identifier for the user.
    # We use UUID for better scalability and to avoid enumeration attacks.
    # Use a string-based UUID column for cross-dialect compatibility (works with SQLite).
    # We store UUIDs as 36-char strings (hex with hyphens) and generate them with uuid.uuid4().
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # User's full name (optional).
    full_name = Column(String, index=True)
    
    # User's email address. Must be unique and is indexed for faster lookups.
    email = Column(String, unique=True, index=True, nullable=False)
    
    # The user's hashed password. It's non-nullable as every user must have one.
    hashed_password = Column(String, nullable=False)
    
    # A flag to indicate if the user's account is active. Defaults to True.
    # This can be used to disable or ban users without deleting their data.
    is_active = Column(Boolean(), default=True)
