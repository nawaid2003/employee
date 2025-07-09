# Replace SQL Server connection with PostgreSQL
import psycopg2
from urllib.parse import urlparse

# Database connection for Render
def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Parse the URL
        url = urlparse(database_url)
        conn = psycopg2.connect(
            host=url.hostname,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            port=url.port
        )
    return conn