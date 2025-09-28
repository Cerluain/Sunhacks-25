from sqlalchemy.orm import declarative_base

# Create a base class for all SQLAlchemy models to inherit from.
# This allows SQLAlchemy's declarative extension to discover all the models.
Base = declarative_base()
