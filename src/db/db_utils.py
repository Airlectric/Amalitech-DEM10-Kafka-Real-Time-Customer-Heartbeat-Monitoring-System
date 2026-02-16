import psycopg2
from psycopg2.extras import execute_values
from src.config.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT
from src.config.logger import get_logger

logger = get_logger("DBUtils")

def get_connection():
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )

def insert_valid_heartbeat(data):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO heartbeats_valid (customer_id, timestamp, heart_rate, anomaly)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (data["customer_id"], data["timestamp"], data["heart_rate"], data.get("anomaly", False))
                )
        logger.info(f"Inserted valid heartbeat: {data}")
    except Exception as e:
        logger.error(f"Error inserting valid heartbeat: {e}", exc_info=True)

def insert_invalid_heartbeat(data, error_reason):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO heartbeats_invalid (customer_id, timestamp, heart_rate, error_reason)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (data.get("customer_id"), data.get("timestamp"), data.get("heart_rate"), error_reason)
                )
        logger.warning(f"Inserted invalid heartbeat: {data} | Reason: {error_reason}")
    except Exception as e:
        logger.error(f"Error inserting invalid heartbeat: {e}", exc_info=True)
