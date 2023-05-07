import datetime
import jdatetime
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from utils.generate_random_number import generate_random_number
from accounts.models import OTPCode
from django.http import JsonResponse
from utils.valid_phone_number import validate_phone_number
from orders.forms import TemplateOrderForm
from django.core.exceptions import ValidationError

def get_jdatetime():
    now = datetime.datetime.now()

    # Convert the current date and time to Persian calendar
    persian_date = jdatetime.date.fromgregorian(date=now)

    # Get the current time in 24-hour format
    time = now.strftime("%H:%M")
    persian_date = persian_date.strftime("%Y/%m/%d")
    persian_time = time
    jdate_time = [persian_date, persian_time]
    return jdate_time


# @csrf_exempt
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
