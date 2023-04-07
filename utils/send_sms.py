from ippanel import Client

api_key = "QIHkyi6cjiZo0UngyEnJ3ybvj82tHO1dgNNyv9iM3DE="

sms = Client(api_key)


def send_verification_sms(phone_number, verification_code):
    pattern_values = {
        "phone": phone_number,
        "verification-code": verification_code,
    }
    sms.send_pattern(
        "mhrpl8zq76fhm48",  # pattern code
        "+3000505",  # originator
        f"{phone_number}",  # recipient
        pattern_values,  # pattern values
    )
    return True


def send_increase_credit_sms(phone_number, amount, credit):
    pattern_values = {
        "amount": amount,
        "credit": credit,
    }
    sms.send_pattern(
        "1cvmuyfqd94fdco",
        "+3000505",
        f"{phone_number}",
        pattern_values,  #
    )
    return True


def send_register_sms(phone_number, verification_code):
    pattern_values = {
        "phone": phone_number,
        "verification-code": verification_code,
    }
    sms.send_pattern(
        "sfmvwa9et09ulfi",
        "+3000505",
        f"{phone_number}",
        pattern_values,
    )
    return True


def send_register_success_sms(phone_number, time):
    pattern_values = {
        "phone": phone_number,
        "time": time,
    }
    sms.send_pattern(
        "9xludp09i5nbj7o",
        "+3000505",
        f"{phone_number}",
        pattern_values,
    )
    return True


def send_submit_ticket_sms(phone_number, ticketCode):
    pattern_values = {
        "ticketCode": ticketCode,
    }
    sms.send_pattern(
        "onk5pwasfyzeopk",
        "+3000505",
        f"{phone_number}",
        pattern_values,
    )
    return True


def send_support_answer_ticket_sms(phone_number, ticketCode):
    pattern_values = {
        "ticketCode": ticketCode,
    }
    sms.send_pattern(
        "4i0wvfb8ertg8qi",
        "+3000505",
        f"{phone_number}",
        pattern_values,
    )
    return True


def send_user_answer_ticket_sms(phone_number, ticketCode):
    pattern_values = {
        "ticketCode": ticketCode,
    }
    sms.send_pattern(
        "w92dmxueobmo7dk",
        "+3000505",
        f"{phone_number}",
        pattern_values,
    )
    return True
