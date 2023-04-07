from accounts.models import User
from django.http import HttpResponse
# from User.models import Order


def fix_phonenumber(request):
    users = User.objects.all()
    for user in users:
        if len(user.phone_number) < 11:
            print(user.phone_number)
            # user.delete()
            # user.save()
        # if user.phone_number.startswith('0'):
        #     pass
        # else:
        #     phone_number = str(user.phone_number)
        #     newphone_number = phone_number.rjust(len(phone_number) + 1, "0")
        #     user.phone_number = newphone_number
        #     user.save()
    return HttpResponse('OK')
