import argparse
import threading
from src.db.db_utils import create_schema
from src.kafka.producer import main as producer_main
from src.kafka.consumer import main as consumer_main
from src.config.logger import get_logger

logger = get_logger("MainEntrypoint")

def run_producer():
    logger.info("Starting Kafka producer...")
    producer_main()

def run_consumer():
    logger.info("Starting Kafka consumer...")
    consumer_main()

def main():
    parser = argparse.ArgumentParser(description="Heartbeat Monitoring System Entrypoint")
    parser.add_argument('--init-db', action='store_true', help='Initialize database schema')
    parser.add_argument('--producer', action='store_true', help='Run Kafka producer')
    parser.add_argument('--consumer', action='store_true', help='Run Kafka consumer')
    parser.add_argument('--both', action='store_true', help='Run both producer and consumer')
    args = parser.parse_args()

    if args.init_db:
        create_schema()

    if args.both:
        t1 = threading.Thread(target=run_producer)
        t2 = threading.Thread(target=run_consumer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    elif args.producer:
        run_producer()
    elif args.consumer:
        run_consumer()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
