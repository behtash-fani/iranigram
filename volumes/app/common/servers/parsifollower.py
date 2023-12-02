import requests
from environs import Env
import json

# for environment variables
env = Env()
env.read_env()

class Parsifollower: # Parsifollower order manager
    def __init__(self):
        self.endpoint = env("PARSIFOLLOWER_ENDPOINT")
        self.api_key = env("PARSIFOLLOWER_API_KEY")

    def submit_order(self, service, link, quantity):
        params = {
            "key": self.api_key,
            "action": "add",
            "service": service,
            "link": link,
            "quantity": quantity,
        }
        response = requests.post(self.endpoint, params=params)
        response = response.content
        submitted_order = json.loads(response.decode('utf-8'))
        return submitted_order

    def order_status(self, server_order_code):
        params = {
            "key": self.api_key,
            "action": "status",
            "order": server_order_code
        }
        response = requests.post(self.endpoint, params=params)
        response = response.content
        order_status = json.loads(response)
        return order_status
    
    def get_service_data(self, service_code):
        params = {
            "key": self.api_key,
            "action": "services",
        }
        r = requests.post(self.endpoint, params=params)
        for item in json.loads(r.content):
            if item['service'] == str(service_code):
                service_data = item
        return service_data
