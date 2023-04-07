import time
import random
from orders.models import Order


def generate_random_number(num, is_unique=None):
    timestamp = int(time.time())
    rand_int = random.randint(10000000, 99999999)
    unique_id = (str(timestamp) + str(rand_int))[-num:]
    if is_unique:
        if check_id_exists(unique_id):
            return generate_random_number(num, is_unique)

    return unique_id


def check_id_exists(unique_id):
    if Order.objects.filter(order_code=unique_id).exists():
        return True
    return False
