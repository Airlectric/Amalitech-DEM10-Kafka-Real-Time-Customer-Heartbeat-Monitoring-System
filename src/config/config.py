import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# PostgreSQL configuration
POSTGRES_USER = os.getenv("POSTGRES_USER", "heartbeat_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "heartbeat_pass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "heartbeat_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))

# Kafka configuration
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "heartbeats")

# Other configuration
CUSTOMER_COUNT = int(os.getenv("CUSTOMER_COUNT", 10))
HEART_RATE_MIN = int(os.getenv("HEART_RATE_MIN", 50))
HEART_RATE_MAX = int(os.getenv("HEART_RATE_MAX", 120))

