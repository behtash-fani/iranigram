import requests
from orders.models import Order


class OrderManager:
    def __init__(self, order_code):
        self.order_code = order_code
        self.endpoint = "https://panel.parsifollower.com/api/v1"
        self.api_key = "sGCcZKIkfsaif7jbq9ibhF5K21n7wCcO"

    def submit_order(self):
        order = Order.objects.get(order_code=self.order_code)
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
        order = Order.objects.get(order_code=self.order_code)
        server_order_code = order.server_order_code
        params = {
            "key": self.api_key,
            "action": "status",
            "order": server_order_code
        }
        response = requests.post(self.endpoint, params=params)
        return response.content
