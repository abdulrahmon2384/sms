"""
Database configuration module for Intelleva School Management System.
Provides fallback to SQLite when AivenCloud PostgreSQL is unavailable.
"""
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import logging
from cryptography.fernet import Fernet
import time
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get database configuration
DB_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
FERNET_KEY = os.getenv("FERNET_KEY")

# Generate a default Fernet key if none exists
if not FERNET_KEY:
    logger.warning("No Fernet key found in .env, generating a new one")
    key = Fernet.generate_key()
    FERNET_KEY = key.decode()
    logger.info(f"Generated new Fernet key: {FERNET_KEY}")

# Initialize encryption
try:
    cipher = Fernet(FERNET_KEY.encode())
    logger.info("Encryption initialized successfully")
except Exception as e:
    logger.error(f"Error initializing encryption: {e}")
    # Generate a new key as fallback
    key = Fernet.generate_key()
    cipher = Fernet(key)
    logger.info("Using fallback encryption key")

# SQLite fallback path
SQLITE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'intelleva.db')
SQLITE_URL = f"sqlite:///{SQLITE_PATH}"

def get_db_engine(max_retries=3, retry_delay=2):
    """
    Attempts to connect to AivenCloud PostgreSQL database.
    Falls back to SQLite if connection fails.
    
    Returns:
        SQLAlchemy engine, is_postgres (boolean)
    """
    # Try to connect to PostgreSQL with retry logic
    for attempt in range(max_retries):
        try:
            logger.info(f"PostgreSQL connection attempt {attempt + 1}/{max_retries}...")
            engine = create_engine(DB_URL)
            conn = engine.connect()
            logger.info("PostgreSQL connection successful!")
            
            # Test query to verify schema functionality
            try:
                result = conn.execute(text('SELECT current_schema()')).fetchone()
                logger.info(f"Current schema: {result[0]}")
            except Exception as e:
                logger.warning(f"Schema query failed: {e}")
                
            conn.close()
            return engine, True
        except Exception as e:
            logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                logger.warning("All PostgreSQL connection attempts failed.")
    
    # Fall back to SQLite
    logger.info(f"Using SQLite fallback at {SQLITE_PATH}")
    engine = create_engine(SQLITE_URL)
    return engine, False

def encrypt_data(data):
    """
    Encrypts data using Fernet symmetric encryption.
    
    Args:
        data: String data to encrypt
        
    Returns:
        Encrypted data as string
    """
    if not data:
        return data
        
    try:
        if isinstance(data, str):
            return cipher.encrypt(data.encode()).decode()
        else:
            return data
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        return data

def decrypt_data(encrypted_data):
    """
    Decrypts data using Fernet symmetric encryption.
    
    Args:
        encrypted_data: Encrypted string data
        
    Returns:
        Decrypted data as string
    """
    if not encrypted_data:
        return encrypted_data
        
    try:
        if isinstance(encrypted_data, str):
            return cipher.decrypt(encrypted_data.encode()).decode()
        else:
            return encrypted_data
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        return encrypted_data

def set_schema(conn, schema_name):
    """
    Sets the PostgreSQL schema for the current connection.
    No-op for SQLite.
    
    Args:
        conn: SQLAlchemy connection
        schema_name: Schema name to set
    """
    try:
        conn.execute(text(f"SET search_path TO {schema_name}"))
        logger.info(f"Schema set to: {schema_name}")
        return True
    except Exception as e:
        logger.warning(f"Failed to set schema: {e}")
        return False

def create_schema_if_not_exists(engine, schema_name):
    """
    Creates a PostgreSQL schema if it doesn't exist.
    No-op for SQLite.
    
    Args:
        engine: SQLAlchemy engine
        schema_name: Schema name to create
    """
    try:
        with engine.connect() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
            logger.info(f"Schema created or verified: {schema_name}")
            return True
    except Exception as e:
        logger.warning(f"Failed to create schema: {e}")
        return False
