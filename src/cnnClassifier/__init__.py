import os
import sys
import logging
import psycopg2
from postgres_database.config import read_config
from psycopg2 import sql

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)


try:
    logging.basicConfig(
        level=logging.INFO,
        format=logging_str,

        handlers=[
            logging.FileHandler(log_filepath),
            logging.StreamHandler(sys.stdout)
        ]
    )
except Exception as e:
    print(f"Error: Unable to configure logger - {e}")
    sys.exit(1)
db_params = read_config()
# Create table if not exists
create_table_query = """
    CREATE TABLE IF NOT EXISTS public.log_table (
        id SERIAL PRIMARY KEY,
        log_level VARCHAR(10),
        module  VARCHAR(50),
        log_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

try:
    # Establish database connection and create table
    with psycopg2.connect(**db_params) as conn, conn.cursor() as cursor:
        cursor.execute(create_table_query)
        conn.commit()

except psycopg2.Error as e:
    print(f"Error: Unable to create table - {e}")
    sys.exit(1)


# Custom log handler to store logs in PostgreSQL
class PostgreSQLHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        try:
            with psycopg2.connect(**db_params) as conn, conn.cursor() as cursor:
                insert_query = sql.SQL("""
                        INSERT INTO public.log_table (log_level, module, log_message) 
                        VALUES (%s, %s, %s)
                    """)
                cursor.execute(insert_query, (record.levelname, record.module, self.format(record)))
                conn.commit()
        except psycopg2.Error as e:
            print(f"Error: Unable to insert log into the database - {e}")


# Add PostgreSQLHandler to the logger
logger = logging.getLogger("cnnClassifierLogger")
logger.addHandler(PostgreSQLHandler())

# Example log messages
try:
    logger.info("This is an informational message.")
    logger.error("This is an error message.")
except Exception as e:
    print(f"Error: Unable to log messages - {e}")
