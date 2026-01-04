"""
Database connection and initialization
"""
import sqlite3
import os
import logging
from contextlib import contextmanager
from typing import Generator
from config import settings

logger = logging.getLogger(__name__)


def init_db():
    """Initialize the database and create tables if they don't exist"""
    try:
        conn = sqlite3.connect(settings.database_path)
        cursor = conn.cursor()
        
        # Create prospects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prospects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                company_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index on email for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_prospects_email ON prospects(email)
        """)
        
        # Create index on created_at for faster sorting
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_prospects_created_at ON prospects(created_at)
        """)
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {settings.database_path}")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Database connection context manager with proper error handling"""
    conn = None
    try:
        conn = sqlite3.connect(settings.database_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Unexpected database error: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_db_connection() -> sqlite3.Connection:
    """Get a database connection (for use without context manager)"""
    conn = sqlite3.connect(settings.database_path)
    conn.row_factory = sqlite3.Row
    return conn

