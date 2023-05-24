import requests
from environs import Env


# for environment variables
env = Env()
env.read_env()

ENDPOINT = "https://api.limosms.com/api/sendpatternmessage"
API_KEY = env("SMS_PANEL_API_KEY")



def send_login_sms(phone_number, verification_code):
    sms_var = [f'{phone_number}', f'{verification_code}']
    params = {'OtpId': '124',
            'ReplaceToken': sms_var,
            'MobileNumber': f'{phone_number}'}
    response = requests.post(ENDPOINT, json=params, headers={"ApiKey": API_KEY})
    return True


def send_register_sms(phone_number, verification_code):
    sms_var = [f'{phone_number}', f'{verification_code}']
    params = {'OtpId': '131',
            'ReplaceToken': sms_var,
            'MobileNumber': f'{phone_number}'}
    response = requests.post(ENDPOINT, json=params, headers={"ApiKey": API_KEY})
    return True


def send_register_success_sms(phone_number, time):
    sms_var = [f'{phone_number}', f'{time}']
    params = {'OtpId': '132',
            'ReplaceToken': sms_var,
            'MobileNumber': f'{phone_number}'}
    response = requests.post(ENDPOINT, json=params, headers={"ApiKey": API_KEY})
    return True


def send_submit_order_sms(phone_number, order_code):
    sms_var = [f'{order_code}']
    params = {'OtpId': '133',
            'ReplaceToken': sms_var,
            'MobileNumber': f'{phone_number}'}
    response = requests.post(ENDPOINT, json=params, headers={"ApiKey": API_KEY})
    return True

def send_cancel_order_sms(phone_number, order_code):
    sms_var = [f'{order_code}']
    params = {'OtpId': '135',
            'ReplaceToken': sms_var,
            'MobileNumber': f'{phone_number}'}
    response = requests.post(ENDPOINT, json=params, headers={"ApiKey": API_KEY})
    return True


def send_increase_credit_sms(phone_number, amount, credit):
    sms_var = [f'{amount}',f'{credit}']
    params = {'OtpId': '139',
            'ReplaceToken': sms_var,
            'MobileNumber': f'{phone_number}'}
    response = requests.post(ENDPOINT, json=params, headers={"ApiKey": API_KEY})
    return True


def send_submit_ticket_sms(phone_number, ticketCode):
    sms_var = [f'{ticketCode}']
    params = {'OtpId': '136',
            'ReplaceToken': sms_var,
            'MobileNumber': f'{phone_number}'}
    response = requests.post(ENDPOINT, json=params, headers={"ApiKey": API_KEY})
    return True


def send_support_answer_ticket_sms(phone_number, ticketCode):
    sms_var = [f'{ticketCode}']
    params = {'OtpId': '137',
            'ReplaceToken': sms_var,
            'MobileNumber': f'{phone_number}'}
    response = requests.post(ENDPOINT, json=params, headers={"ApiKey": API_KEY})
    return True


def send_user_answer_ticket_sms(phone_number, ticketCode):
    sms_var = [f'{ticketCode}']
    params = {'OtpId': '138',
            'ReplaceToken': sms_var,
            'MobileNumber': f'{phone_number}'}
    response = requests.post(ENDPOINT, json=params, headers={"ApiKey": API_KEY})
    return True


