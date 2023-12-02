import re

def validate_phone_number(phone_number):
    phone_number = phone_number.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))
    
    # Corrected Iran phone pattern
    correct_iran_phone_pattern = r'^(0|98|\+98|0098)-?9-?\d{9}$'

    # Check if the phone number matches the standard pattern
    if re.match(correct_iran_phone_pattern, phone_number):
        return phone_number

    # Check for alternative formats and replace them with '0'
    for exp in ['98', r'\+98', r'\+980', r'0098', r'098', r'00980']:
        if re.match(f"^{exp}", phone_number):
            phone_number = re.sub(f"^{exp}", "0", phone_number)
            return phone_number

    return False
