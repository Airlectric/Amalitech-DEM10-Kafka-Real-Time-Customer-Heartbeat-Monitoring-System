import json
import time
from kafka import KafkaProducer
from src.data.data_generator import generate_heartbeat
from src.config.config import KAFKA_BROKER, KAFKA_TOPIC
from src.config.logger import get_logger

logger = get_logger("KafkaProducer")


# Producer with idempotence and durability, but sends messages continuously
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',  # Wait for all replicas
    enable_idempotence=True,  # Prevent duplicates
)

def main():
    logger.info(f"Producing to Kafka topic '{KAFKA_TOPIC}' at broker '{KAFKA_BROKER}'...")
    try:
        while True:
            event = generate_heartbeat()
            producer.send(KAFKA_TOPIC, event).add_callback(on_send_success).add_errback(on_send_error)
            time.sleep(1)  # Simulate real-time
    except KeyboardInterrupt:
        logger.info("Producer stopped.")
    finally:
        producer.flush()
        producer.close()

def on_send_success(record_metadata):
    logger.info(f"Message sent to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")

def on_send_error(excp):
    logger.error(f"Send failed: {excp}", exc_info=True)

if __name__ == "__main__":
    main()
