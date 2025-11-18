import logging
from contextlib import contextmanager
from typing import Optional, Generator

# DB Interface, Repo and Config Classes
from src.db.postgresql.config import PostgreSQLSettings
from src.db.interfaces.base import BaseDatabase

# SQLAlchemy Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


## Setup a Basic Logger
logger = logging.getLogger(__name__)

# SQLAlcehmy Declarative Base
Base = declarative_base()

class PostgreSQLDatabase(BaseDatabase):
    """
    PostgreSQL Database Implementation
    """
    def __init__(self, dbconfig:PostgreSQLSettings):
        self.config = dbconfig
        self.engine: Optional[Engine] = None
        self.session_factory: Optional[sessionmaker] = None
    
    def startup(self) -> None:
        """
        Initialize the Database Connection
        """
        try:
            # Log Connection Attempt
            logger.info(
                f"Attempting to connect to PostgreSQL at: {self.config.database_url.split('@')[1] if '@' in self.config.database_url else 'localhost'}"
            )

            # Create DB Engine
            self.engine = create_engine(
                self.config.database_url,
                echo = self.config.echo_sql,
                pool_size = self.config.pool_size,
                max_overflow= self.config.max_overflow,
                pool_pre_ping=True #Verify Connections before Use
            )

            # DB Sessions
            self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)

            # Test the Connection
            assert self.engine is not None
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("Database connection test successful")
            
            # Check which tables exist before creating
            inspector = inspect(self.engine)
            existing_tables = inspector.get_table_names()

            # Create tables if they don't exist (Idempotent Operation)
            Base.metadata.create_all(bind=self.engine)

            # Check if any new tables were created
            updated_tables = inspector.get_table_names()
            new_tables = set(updated_tables) - set(existing_tables)
            if new_tables:
                logger.info(f"Created new tables: {" ".join(new_tables)}")
            else:
                logger.info("All tables already exist - no new tables created")
            
            logger.info("PostgreSQL database initialized successfully")
            assert self.engine is not None
            logger.info(f"Database: {self.engine.url.database}")
            logger.info(f"Total tables: {', '.join(updated_tables) if updated_tables else 'None'}")
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL database: {e}")
            raise
    

    def teardown(self):
        """Close the database connection"""
        if self.engine:
            self.engine.dispose()
            logger.info("PostgreSQL database connections closed")
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session."""
        if not self.session_factory:
            raise RuntimeError("Database not initialized. Call startup() first.")
        session = self.session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()



