import requests
from orders.models import Order
from environs import Env

# for environment variables
env = Env()
env.read_env()

class PFOrderManager: # Parsifollower order manager
    def __init__(self, order_id):
        self.order_id = order_id
        self.endpoint = env("PARSIFOLLOWER_ENDPOINT")
        self.api_key = env("PARSIFOLLOWER_API_KEY")

    def submit_order(self):
        order = Order.objects.get(id=self.order_id)
        params = {
            "key": self.api_key,
            "action": "add",
            "service": order.service.server_service_code,
            "link": order.link,
            "quantity": order.quantity,
        }
        response = requests.post(self.endpoint, params=params)
        return response.content

    def order_status(self):
        order = Order.objects.get(id=self.order_id)
        server_order_code = order.server_order_code
        params = {
            "key": self.api_key,
            "action": "status",
            "order": server_order_code
        }
        response = requests.post(self.endpoint, params=params)
        return response.content
