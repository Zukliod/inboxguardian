import os
import psycopg2
from urllib.parse import urlparse

def get_db_connection():
    # Use DATABASE_URL from environment variables
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is not set in the environment variables.")
    
    result = urlparse(database_url)
    connection = psycopg2.connect(
        host=result.hostname,
        port=result.port,
        user=result.username,
        password=result.password,
        dbname=result.path[1:]  # Remove leading '/'
    )
    return connection