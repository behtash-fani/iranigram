import requests
from decouple import config
import json


class Berlia: # Berlia order manager
    def __init__(self):
        self.endpoint = config("BERLIA_ENDPOINT")
        self.api_key = config("BERLIA_API_KEY")

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
        submitted_order = json.loads(response.decode("utf-8"))
        return submitted_order

    def order_status(self,server_order_code):
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
        try:
            r = requests.get(self.endpoint, params=params)
            r.raise_for_status()
            data = r.json()
            service_data = next((item for item in data if item.get('service') == str(service_code)), None)
            return service_data
        except requests.RequestException as e:
            return None
