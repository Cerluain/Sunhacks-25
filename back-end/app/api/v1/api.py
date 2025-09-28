# --- Imports ---
# Import FastAPI to create the main application instance.
from fastapi import FastAPI
# Import the routers from the endpoints modules.
from app.api.v1.endpoints import auth as auth_router
from app.api.v1.endpoints import users as user_router

# --- FastAPI App Instantiation ---
# Create an instance of the FastAPI class. This will be the main entry point for your API.
# The title and version are useful for API documentation (e.g., at /docs).
app = FastAPI(
    title="My Secure FastAPI Application",
    version="1.0.0",
)

# --- Include Routers ---
# Include the authentication router.
# All routes defined in the auth module will be prefixed with /api/v1.
# For example, the /token route in auth.py will become /api/v1/auth/token.
app.include_router(auth_router.router, prefix="/api/v1")

# Include the user management router.
# This will make routes like a user creation endpoint available under the /api/v1 prefix.
# For example, a /users route in users.py will become /api/v1/users.
app.include_router(user_router.router, prefix="/api/v1")

# --- Root Endpoint ---
# A simple root endpoint to confirm the API is running.
@app.get("/", tags=["Root"])
async def read_root():
    """
    A simple endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the API!"}
