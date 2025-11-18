from src.config import get_settings
from src.db.interfaces.base import BaseDatabase
from src.db.postgresql.config import PostgreSQLSettings
from src.db.postgresql.connection import PostgreSQLDatabase

def make_database() -> BaseDatabase:
    """
    Factor Function to create a database instance
    """
    #Get settings from centralized config
    settings = get_settings()

    #Create PostgreSQL config from settings
    config = PostgreSQLSettings(
        database_url=settings.postgres_database_url,
        echo_sql=settings.postgres_echo_sql,
        pool_size=settings.postgres_pool_size,
        max_overflow=settings.postgres_max_overflow,
    )

    database = PostgreSQLDatabase(dbconfig=config)
    database.startup()
    return database
