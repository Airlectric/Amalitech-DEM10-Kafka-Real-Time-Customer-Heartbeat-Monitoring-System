import json
import threading
from kafka import KafkaConsumer
from src.config.config import KAFKA_BROKER, KAFKA_TOPIC, HEART_RATE_MIN, HEART_RATE_MAX
from src.config.logger import get_logger
from src.db.db_utils import insert_heartbeat_event, insert_alert

logger = get_logger("KafkaConsumer")

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=False,  # Manual commit for durability
    max_poll_records=100,  # Batch processing
    consumer_timeout_ms=1000,
    group_id='heartbeat-consumer-group'  # Required for manual commits
)



# New validation and anomaly classification logic
def classify_heartbeat(event):
    try:
        hr = event.get("heartbeat_value")
        if hr is None:
            return {
                "validation_status": "invalid_system",
                "anomaly_type": "null_value",
                "alert_category": "system_anomaly"
            }
        if not isinstance(hr, (int, float)):
            return {
                "validation_status": "corrupted",
                "anomaly_type": "parsing_error",
                "alert_category": "data_corruption"
            }
        if hr < 0:
            return {
                "validation_status": "invalid_system",
                "anomaly_type": "negative_value",
                "alert_category": "system_anomaly"
            }
        if hr > 300:
            return {
                "validation_status": "invalid_system",
                "anomaly_type": "overflow_value",
                "alert_category": "system_anomaly"
            }
        if hr < HEART_RATE_MIN:
            return {
                "validation_status": "invalid_physiological",
                "anomaly_type": "low_bpm",
                "alert_category": "physiological_anomaly"
            }
        if hr > HEART_RATE_MAX:
            return {
                "validation_status": "invalid_physiological",
                "anomaly_type": "high_bpm",
                "alert_category": "physiological_anomaly"
            }
        # Valid
        return {
            "validation_status": "valid",
            "anomaly_type": None,
            "alert_category": None
        }
    except Exception:
        return {
            "validation_status": "corrupted",
            "anomaly_type": "parsing_error",
            "alert_category": "data_corruption"
        }



def process_batch(messages):
    for msg in messages:
        raw = msg.value
        # Always store the raw payload
        event = {
            "timestamp": raw.get("timestamp"),
            "patient_id": raw.get("patient_id"),
            "heartbeat_value": raw.get("heartbeat_value"),
            "raw_payload": raw
        }
        classification = classify_heartbeat(event)
        event["validation_status"] = classification["validation_status"]
        event["anomaly_type"] = classification["anomaly_type"]
        heartbeat_id = insert_heartbeat_event(event)
        if event["validation_status"] != "valid" and heartbeat_id:
            insert_alert(heartbeat_id, event, classification["alert_category"])

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
