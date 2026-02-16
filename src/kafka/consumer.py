import json
import threading
from kafka import KafkaConsumer
from src.config.config import KAFKA_BROKER, KAFKA_TOPIC, HEART_RATE_MIN, HEART_RATE_MAX
from src.config.logger import get_logger
from src.db.db_utils import insert_valid_heartbeat, insert_invalid_heartbeat

logger = get_logger("KafkaConsumer")

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=False,  # Manual commit for durability
    max_poll_records=100,  # Batch processing
    consumer_timeout_ms=1000
)

def validate_heartbeat(data):
    hr = data.get("heart_rate")
    if hr is None:
        return False, "Missing heart_rate"
    if not (HEART_RATE_MIN <= hr <= HEART_RATE_MAX):
        return False, f"Heart rate out of range: {hr}"
    return True, None

def process_batch(messages):
    for msg in messages:
        heartbeat = msg.value
        valid, reason = validate_heartbeat(heartbeat)
        if valid:
            insert_valid_heartbeat(heartbeat)
        else:
            insert_invalid_heartbeat(heartbeat, reason)

def main():
    logger.info(f"Consuming from Kafka topic '{KAFKA_TOPIC}' at broker '{KAFKA_BROKER}'...")
    try:
        while True:
            messages = consumer.poll(timeout_ms=1000, max_records=100)
            for tp, batch in messages.items():
                process_batch(batch)
                consumer.commit()  # Manual commit after batch
    except KeyboardInterrupt:
        logger.info("Consumer stopped.")
    except Exception as e:
        logger.error(f"Consumer error: {e}", exc_info=True)
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
