from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Manages application settings, loading them from environment variables.
    It will automatically look for a .env file in the project root.
    """
    # --- JWT Settings ---
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- Database Settings ---
    DATABASE_URL: str

    # This tells pydantic-settings to load variables from a .env file.
    model_config = SettingsConfigDict(env_file=".env")

# Create a single, reusable instance of the settings.
# Other modules can import this `settings` object to access configuration.
settings = Settings()

