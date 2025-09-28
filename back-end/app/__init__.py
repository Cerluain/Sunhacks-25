"""
Main application package for the back-end API.

This package contains all the core components of the application including:
- AI/LLM functionality
- API endpoints and routing
- Database models and schemas
- CRUD operations
- Core configuration and utilities
"""

__version__ = "0.1.0"
__author__ = "Sunhacks Team"

# Import core configuration
try:
    from .core.config import settings
except ImportError:
    settings = None

# Import database components
try:
    from .db.session import SessionLocal, engine, get_db
except ImportError:
    SessionLocal = engine = get_db = None

# Import models - make them available at app level
try:
    from .models import *
    from .models.llm_schemas import LLMResponse, Source
except ImportError:
    pass

# Import schemas
try:
    from .schemas import *
except ImportError:
    pass

# Import CRUD operations
try:
    from .crud import *
except ImportError:
    pass

# Define what gets imported when someone does "from app import *"
__all__ = [
    # Core
    "settings",
    
    # Database
    "SessionLocal",
    "engine", 
    "get_db",
    
    # Models
    "LLMResponse",
    "Source",
    
    # Version info
    "__version__",
    "__author__",
]

def get_app_info():
    """Get basic information about the application."""
    return {
        "name": "Sunhacks Backend API",
        "version": __version__,
        "author": __author__,
        "description": "Backend API for the Sunhacks project with AI/LLM capabilities"
    }