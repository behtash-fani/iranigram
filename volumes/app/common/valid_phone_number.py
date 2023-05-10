import re


def validate_phone_number(phone_number):
    phone_number = phone_number.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))
    correct_iran_phone_pattern = r'^(?:0|98|\+98|\+980|0098|098|00980)-?9-?\d{9}$'

    if re.search(r'^(0)-?9-?\d{9}$', phone_number):
        return phone_number
    if re.search(correct_iran_phone_pattern, phone_number):
        for exp in ['98', '\+98', '\+980', '0098', '098', '00980']:
            if re.search(f"^({exp})", phone_number):
                phone_number = re.sub(f"^({exp})", "0", phone_number)
                return phone_number
    return False