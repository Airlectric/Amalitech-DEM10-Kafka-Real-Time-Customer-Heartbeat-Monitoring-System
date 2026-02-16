import random
import string
from datetime import datetime
from src.config.config import CUSTOMER_COUNT, HEART_RATE_MIN, HEART_RATE_MAX, INVALID_HEART_RATE_MIN, INVALID_HEART_RATE_MAX

CUSTOMER_IDS = [
    ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    for _ in range(CUSTOMER_COUNT)
]

def generate_heartbeat():
    customer_id = random.choice(CUSTOMER_IDS)
    timestamp = datetime.utcnow().isoformat()
    # 80% valid, 20% invalid
    if random.random() < 0.8:
        heartbeat_value = random.randint(HEART_RATE_MIN, HEART_RATE_MAX)
    else:
    # Generate invalid heart rate
        if random.random() < 0.5:
            heartbeat_value = random.randint(-20, HEART_RATE_MIN - 1)  # can be negative for system anomaly
        else:
            heartbeat_value = random.randint(HEART_RATE_MAX + 1, 350)  # can be overflow for system anomaly
    return {
        "patient_id": patient_id,
        "timestamp": timestamp,
        "heartbeat_value": heartbeat_value
    }

if __name__ == "__main__":
    for _ in range(10):
        print(generate_heartbeat())
