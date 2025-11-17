import logging

from pydantic import Field
from pydantic_settings import BaseSettings

## Initiate Standard/Basic Logger
logger = logging.getLogger(__name__)

class PostgreSQLSettings(BaseSettings):
    """PostgreSQL Configuration Settings"""
    database_url: str = Field(
        default="postgresql://rag_user:rag_password@localhost:5432/rag_db",
        description="PostgreSQL Database URL")
    echo_sql: bool = Field(default=False, description="Enable SQL Query Logging")
    pool_size: int = Field(default=20, description="Database Connection Pool Size")
    max_overflow: int = Field(default=0, description="Maximum Pool Overflow")

    class Config:
        env_prefix = "POSTGRES_"

dbconfig = PostgreSQLSettings()
