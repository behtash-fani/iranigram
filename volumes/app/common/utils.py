from accounts.tasks import send_login_sms_task
from common.generate_random_number import generate_random_number
from common.valid_phone_number import validate_phone_number
from datetime import datetime, timedelta
from django.http import JsonResponse
from accounts.models import OTPCode

def send_otpcode_again(request):
    phone_number = request.POST.get("phone_number")
    phone_number = validate_phone_number(phone_number)
    if phone_number == False:
        return JsonResponse({"Status": "wrong_phone_number"})
    link = request.POST.get("link")
    request.session["phone_number"] = phone_number
    request.session["link"] = link
    verification_code = generate_random_number(4, is_unique=False)
    if OTPCode.objects.filter(phone_number=phone_number).exists():
        OTPCode.objects.get(phone_number=phone_number).delete()
    OTPCode.objects.create(
                phone_number=phone_number,
                code=verification_code,
                expire_time=datetime.now() + timedelta(seconds=60),
            )
    return JsonResponse({"Status": "code_sent"})
