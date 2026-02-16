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


# Insert a heartbeat event into the heartbeats table (new schema)
def insert_heartbeat_event(data):
    conn = get_connection()
    heartbeat_id = None
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO heartbeats (timestamp, patient_id, heartbeat_value, validation_status, anomaly_type, raw_payload)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        data["timestamp"],
                        data["patient_id"],
                        data.get("heartbeat_value"),
                        data["validation_status"],
                        data.get("anomaly_type"),
                        data.get("raw_payload")
                    )
                )
                heartbeat_id = cur.fetchone()[0]
        logger.info(f"Inserted heartbeat event: {data}")
        return heartbeat_id
    except Exception as e:
        logger.error(f"Error inserting heartbeat event: {e}", exc_info=True)
        return None
    finally:
        put_connection(conn)

# Insert an alert for a rule violation (new schema)
def insert_alert(heartbeat_id, data, alert_category):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO heartbeat_alerts (heartbeat_id, timestamp, patient_id, heartbeat_value, alert_category)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        heartbeat_id,
                        data["timestamp"],
                        data["patient_id"],
                        data.get("heartbeat_value"),
                        alert_category
                    )
                )
        logger.warning(f"Inserted alert for heartbeat_id={heartbeat_id}: {alert_category}")
    except Exception as e:
        logger.error(f"Error inserting alert: {e}", exc_info=True)
    finally:
        put_connection(conn)
