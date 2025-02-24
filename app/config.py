from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Postgres Database
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST : str
    DB_PORT: int
    DB_NAME : str
    DB_SSL: str

    # LLM API
    OPENAI_API_KEY: str
    GROQ_API_KEY: str

    # Load environment variables from .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()