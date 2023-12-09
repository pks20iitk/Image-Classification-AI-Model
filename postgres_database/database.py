# database.py
import psycopg2


def execute_query(conn, query):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return result
    except psycopg2.Error as e:
        print(e)
        return None


def connect_to_database(params):
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        return conn
    except psycopg2.Error as e:
        print(e)
        return None


def close_connection(conn):
    if conn is not None:
        conn.close()
        print('Database connection closed.')
