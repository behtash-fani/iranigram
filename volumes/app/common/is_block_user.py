from accounts.models import User


def is_block_user(phone_number):
    phone_number = phone_number
    user = User.objects.filter(phone_number=phone_number)
    if user.exists():
        if User.objects.get(phone_number=phone_number).is_block:
            return True
    return False