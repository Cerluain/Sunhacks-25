# --- Imports ---
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the application settings
from app.core.config import settings

# --- Database Engine Setup ---
# Create the SQLAlchemy engine, which is the entry point to the database.
# The 'connect_args' is needed specifically for SQLite to allow it to be used
# by multiple threads, which is the case in a web application.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# --- SessionLocal Class ---
# Create a SessionLocal class using sessionmaker.
# An instance of SessionLocal will be a single database session.
# We configure it here but instantiate it for each request in the dependencies.
# - autocommit=False: We want to manually commit transactions.
# - autoflush=False: We will manually flush data to the DB.
# - bind=engine: This session factory will create sessions bound to our database engine.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
