from config.database_config import get_db_connection

def test_get_db_connection():
    try:
        connection = get_db_connection()
        assert connection is not None, "Database connection failed"
        connection.close()
    except Exception as e:
        assert False, f"Database connection test failed: {e}"