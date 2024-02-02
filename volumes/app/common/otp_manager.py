from accounts.tasks import send_login_sms_task, send_register_sms_task
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from accounts.models import OTPCode
from orders.models import Order
import random
import time
import re


class OTPManager:

    @classmethod
    def login_with_otp(cls, phone_number):
        validated_phone_number, verification_code = OTPManager._prepare_otp(
            phone_number)
        if validated_phone_number and verification_code:
            expire_time = datetime.now() + timedelta(seconds=60)
            OTPCode.objects.create(
                phone_number=validated_phone_number,
                code=verification_code,
                expire_time=expire_time,
            )
            send_login_sms_task.delay(phone_number, verification_code)
            return True
        return False

    @classmethod
    def register_with_otp(cls, phone_number):
        validated_phone_number, verification_code = cls._prepare_otp(
            phone_number)
        if validated_phone_number and verification_code:
            expire_time = datetime.now() + timedelta(seconds=60)
            OTPCode.objects.create(
                phone_number=validated_phone_number,
                code=verification_code,
                expire_time=expire_time,
            )
            send_register_sms_task.delay(phone_number, verification_code)

    @classmethod
    def _prepare_otp(cls, phone_number):
        raw_phone_number = phone_number
        validated_phone_number = cls.validate_phone_number(raw_phone_number)
        OTPCode.objects.filter(phone_number=validated_phone_number).delete()
        verification_code = cls.generate_random_number(4, is_unique=False)
        return validated_phone_number, verification_code

    @staticmethod
    def validate_phone_number(phone_number):
        if not phone_number.isdigit():
            return False
        phone_number = phone_number.translate(
            str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))
        correct_iran_phone_pattern = r'^(0|98|\+98|0098)-?9-?\d{9}$'
        if re.match(correct_iran_phone_pattern, phone_number):
            return phone_number
        for exp in ['98', r'\+98', r'\+980', r'0098', r'098', r'00980']:
            if re.match(f"^{exp}", phone_number):
                phone_number = re.sub(f"^{exp}", "0", phone_number)
                return phone_number
        return False

    @staticmethod
    def generate_random_number(length, is_unique):
        timestamp = int(time.time())
        rand_int = random.randint(10000000, 99999999)
        unique_id = (str(timestamp) + str(rand_int))[-length:]
        if is_unique:
            while OTPManager.check_id_exists(unique_id):   
                unique_id = OTPManager.generate_random_number(length, is_unique)
        return unique_id

    @staticmethod
    def check_id_exists(unique_id):
        if Order.objects.filter(order_code=unique_id).exists():
            return True
        return False

    @staticmethod
    def verify_otpcode(phone_number, code):
        try:
            verification_code = OTPCode.objects.get(phone_number=phone_number)
            if code and code.isdigit():
                if int(code) == int(verification_code.code):
                    verification_code.delete()
                    return True
                else:
                    return False
            else:
                return False
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def check_expire_time(phone_number):
        otpcode = OTPCode.objects.filter(phone_number=phone_number)[0]
        if OTPCode.objects.filter(phone_number=phone_number).exists():
            otp_expiry_time = otpcode.expire_time
            current_time = datetime.now().time()
            current_time_timedelta = timedelta(
                hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second)
            otp_expiry_time_timedelta = timedelta(
                hours=otp_expiry_time.hour, minutes=otp_expiry_time.minute, seconds=otp_expiry_time.second)
            current_time_seconds = current_time_timedelta.total_seconds()
            otp_expiry_time_seconds = otp_expiry_time_timedelta.total_seconds()
            difference_in_minutes = int(
                otp_expiry_time_seconds) - int(current_time_seconds)
            if difference_in_minutes <= 0:
                otpcode.delete()
            return difference_in_minutes
        return False
