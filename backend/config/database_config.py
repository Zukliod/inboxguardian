DATABASE = {
    "host": "localhost",         # Database host (localhost if on your own machine)
    "port": "5432",              # Default PostgreSQL port
    "user": "harshit",     # Replace with your PostgreSQL username
    "password": "Zukliod2.0", # Replace with your PostgreSQL password
    "dbname": "inboxguardian"    # Database name you created earlier
}
import psycopg2

def get_db_connection():
    db_config = DATABASE
    connection = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        dbname=db_config["dbname"]
    )
    return connection