from django.core.cache import cache
import requests
from environs import Env
import json

# for environment variables
env = Env()
env.read_env()


def store_token_sms():
    url = "http://RestfulSms.com/api/Token"
    payload = json.dumps(
        {"UserApiKey": "b2d30f228ccd7e1ec3b71801", "SecretKey": "6590"}
    )
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload)
    token = json.loads(response.text)["TokenKey"]
    cache.set("sms_token", token, 1800)
    return "Ok!"


def retrieve_token():
    token = cache.get("sms_token")
    return token


def check_token_exists():
    if cache.has_key("sms_token"):
        return True
    else:
        return False


def send_login_sms(phone_number, verification_code):
    url = "http://RestfulSms.com/api/UltraFastSend"
    payload = json.dumps(
        {
            "ParameterArray": [
                {"Parameter": "phone", "ParameterValue": f"{phone_number}"},
                {
                    "Parameter": "verification-code",
                    "ParameterValue": f"{verification_code}",
                },
            ],
            "Mobile": f"{phone_number}",
            "TemplateId": "76039",
        }
    )
    if check_token_exists():
        token = retrieve_token()
    else:
        store_token_sms()
        token = retrieve_token()
    headers = {
        "Content-Type": "application/json",
        "x-sms-ir-secure-token": f"{token}",
    }
    requests.request("POST", url, headers=headers, data=payload)
    return True


def send_register_sms(phone_number, verification_code):
    url = "http://RestfulSms.com/api/UltraFastSend"
    payload = json.dumps(
        {
            "ParameterArray": [
                {"Parameter": "phone", "ParameterValue": f"{phone_number}"},
                {
                    "Parameter": "verification-code",
                    "ParameterValue": f"{verification_code}",
                },
            ],
            "Mobile": f"{phone_number}",
            "TemplateId": "76041",
        }
    )
    if check_token_exists():
        token = retrieve_token()
    else:
        store_token_sms()
        token = retrieve_token()
    headers = {
        "Content-Type": "application/json",
        "x-sms-ir-secure-token": f"{token}",
    }
    requests.request("POST", url, headers=headers, data=payload)
    return True


def send_register_success_sms(phone_number, time):
    url = "http://RestfulSms.com/api/UltraFastSend"
    payload = json.dumps(
        {
            "ParameterArray": [
                {"Parameter": "phone", "ParameterValue": f"{phone_number}"},
                {
                    "Parameter": "time",
                    "ParameterValue": f"{time}",
                },
            ],
            "Mobile": f"{phone_number}",
            "TemplateId": "76042",
        }
    )
    if check_token_exists():
        token = retrieve_token()
    else:
        store_token_sms()
        token = retrieve_token()
    headers = {
        "Content-Type": "application/json",
        "x-sms-ir-secure-token": f"{token}",
    }
    requests.request("POST", url, headers=headers, data=payload)
    return True


def send_submit_order_sms(phone_number, order_code):
    url = "http://RestfulSms.com/api/UltraFastSend"
    payload = json.dumps(
        {
            "ParameterArray": [
                {"Parameter": "orderCode", "ParameterValue": f"{order_code}"},
            ],
            "Mobile": f"{phone_number}",
            "TemplateId": "76043",
        }
    )
    if check_token_exists():
        token = retrieve_token()
    else:
        store_token_sms()
        token = retrieve_token()
    headers = {
        "Content-Type": "application/json",
        "x-sms-ir-secure-token": f"{token}",
    }
    requests.request("POST", url, headers=headers, data=payload)
    return True


def send_cancel_order_sms(phone_number, order_code):
    url = "http://RestfulSms.com/api/UltraFastSend"
    payload = json.dumps(
        {
            "ParameterArray": [
                {"Parameter": "orderCode", "ParameterValue": f"{order_code}"},
            ],
            "Mobile": f"{phone_number}",
            "TemplateId": "76045",
        }
    )
    if check_token_exists():
        token = retrieve_token()
    else:
        store_token_sms()
        token = retrieve_token()
    headers = {
        "Content-Type": "application/json",
        "x-sms-ir-secure-token": f"{token}",
    }
    requests.request("POST", url, headers=headers, data=payload)
    return True


def send_increase_credit_sms(phone_number, amount, credit):
    url = "http://RestfulSms.com/api/UltraFastSend"
    payload = json.dumps(
        {
            "ParameterArray": [
                {"Parameter": "amount", "ParameterValue": f"{amount}"},
                {
                    "Parameter": "credit",
                    "ParameterValue": f"{credit}",
                },
            ],
            "Mobile": f"{phone_number}",
            "TemplateId": "76049",
        }
    )
    if check_token_exists():
        token = retrieve_token()
    else:
        store_token_sms()
        token = retrieve_token()
    headers = {
        "Content-Type": "application/json",
        "x-sms-ir-secure-token": f"{token}",
    }
    requests.request("POST", url, headers=headers, data=payload)
    return True


def send_submit_ticket_sms(phone_number, ticketCode):
    url = "http://RestfulSms.com/api/UltraFastSend"
    payload = json.dumps(
        {
            "ParameterArray": [
                {"Parameter": "ticketCode", "ParameterValue": f"{ticketCode}"},
            ],
            "Mobile": f"{phone_number}",
            "TemplateId": "76046",
        }
    )
    if check_token_exists():
        token = retrieve_token()
    else:
        store_token_sms()
        token = retrieve_token()
    headers = {
        "Content-Type": "application/json",
        "x-sms-ir-secure-token": f"{token}",
    }
    requests.request("POST", url, headers=headers, data=payload)
    return True


def send_support_answer_ticket_sms(phone_number, ticketCode):
    url = "http://RestfulSms.com/api/UltraFastSend"
    payload = json.dumps(
        {
            "ParameterArray": [
                {"Parameter": "ticketCode", "ParameterValue": f"{ticketCode}"},
            ],
            "Mobile": f"{phone_number}",
            "TemplateId": "76047",
        }
    )
    if check_token_exists():
        token = retrieve_token()
    else:
        store_token_sms()
        token = retrieve_token()
    headers = {
        "Content-Type": "application/json",
        "x-sms-ir-secure-token": f"{token}",
    }
    requests.request("POST", url, headers=headers, data=payload)
    return True


def send_user_answer_ticket_sms(phone_number, ticketCode):
    url = "http://RestfulSms.com/api/UltraFastSend"
    payload = json.dumps(
        {
            "ParameterArray": [
                {"Parameter": "ticketCode", "ParameterValue": f"{ticketCode}"},
            ],
            "Mobile": f"{phone_number}",
            "TemplateId": "76048",
        }
    )
    if check_token_exists():
        token = retrieve_token()
    else:
        store_token_sms()
        token = retrieve_token()
    headers = {
        "Content-Type": "application/json",
        "x-sms-ir-secure-token": f"{token}",
    }
    requests.request("POST", url, headers=headers, data=payload)
    return True
