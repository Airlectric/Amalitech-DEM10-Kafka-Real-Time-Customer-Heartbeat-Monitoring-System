import psycopg2
from psycopg2.extras import execute_values
from src.config.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT
from src.config.logger import get_logger

import os

logger = get_logger("DBUtils")

# Connection pool for efficiency
from psycopg2 import pool
pg_pool = pool.SimpleConnectionPool(1, 10,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)

def get_connection():
    return pg_pool.getconn()

def put_connection(conn):
    pg_pool.putconn(conn)


def create_schema():
    """Create database tables from schema.sql file"""
    # Get the path to schema.sql (relative to project root)
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    schema_path = os.path.join(current_dir, 'db', 'schema.sql')
    
    conn = get_connection()
    try:
        # Read SQL from file
        with open(schema_path, 'r') as f:
            sql = f.read()
        
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                
        logger.info(f"Database schema created successfully from {schema_path}")
    except Exception as e:
        logger.error(f"Error creating schema: {e}", exc_info=True)
        raise
    finally:
        put_connection(conn)


# Ensure uniqueness for idempotency: add a unique constraint on (customer_id, timestamp) in the DB for production
def insert_valid_heartbeat(data):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO heartbeats_valid (customer_id, timestamp, heart_rate, anomaly)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (customer_id, timestamp) DO NOTHING
                    """,
                    (data["customer_id"], data["timestamp"], data["heart_rate"], data.get("anomaly", False))
                )
        logger.info(f"Inserted valid heartbeat: {data}")
    except Exception as e:
        logger.error(f"Error inserting valid heartbeat: {e}", exc_info=True)
    finally:
        put_connection(conn)

def insert_invalid_heartbeat(data, error_reason):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO heartbeats_invalid (customer_id, timestamp, heart_rate, error_reason)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (customer_id, timestamp) DO NOTHING
                    """,
                    (data.get("customer_id"), data.get("timestamp"), data.get("heart_rate"), error_reason)
                )
        logger.warning(f"Inserted invalid heartbeat: {data} | Reason: {error_reason}")
    except Exception as e:
        logger.error(f"Error inserting invalid heartbeat: {e}", exc_info=True)
    finally:
        put_connection(conn)
