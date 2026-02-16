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
        heart_rate = random.randint(HEART_RATE_MIN, HEART_RATE_MAX)
        valid = True
    else:
        # Generate invalid heart rate
        if random.random() < 0.5:
            heart_rate = random.randint(INVALID_HEART_RATE_MIN, HEART_RATE_MIN - 1)
        else:
            heart_rate = random.randint(HEART_RATE_MAX + 1, INVALID_HEART_RATE_MAX)
        valid = False
    return {
        "customer_id": customer_id,
        "timestamp": timestamp,
        "heart_rate": heart_rate,
        "valid": valid
    }

if __name__ == "__main__":
    for _ in range(10):
        print(generate_heartbeat())
