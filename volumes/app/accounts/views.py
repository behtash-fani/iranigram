from django.forms import ValidationError
from .forms import (
    VerifyCodeForm,
    LoginWithPasswordForm,
    LoginWithOTPForm,
    EditProfileForm,
    AddCreditForm,
    UserRegisterWithOTPForm,
    ChangePasswordForm,
)
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views import View
from .models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from orders.models import Order
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout, login
from support.models import Ticket
from accounts.mixins import BlockCheckLoginRequiredMixin
# from .tasks import send_register_success_sms_task
from common.otp_manager import OTPManager
from django.conf import settings
from rest_framework.authtoken.models import Token
from service.models import Service
import logging


otp_manager = OTPManager()
logger = logging.getLogger(__name__)


class UserDashboardView(BlockCheckLoginRequiredMixin, View):
    template_name = "accounts/dashboard.html"

    def get(self, request):
        user = request.user
        orders_count = Order.objects.filter(user=user).count()
        ticket_count = Ticket.objects.filter(user=user).count()
        context = {"orders_count": orders_count, "ticket_count": ticket_count}
        return render(request, self.template_name, context)


class UserRegisterWithOTPView(View):
    form_class = UserRegisterWithOTPForm
    template_name = "accounts/registration/register.html"
    success_message = _("A one-time password has been sent")

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("accounts:user_dashboard")
        register_form = self.form_class
        context = {"register_form": register_form}
        return render(request, self.template_name, context)

    def post(self, request):
        register_form = self.form_class(request.POST)
        if register_form.is_valid():
            cd = register_form.cleaned_data
            request.session["phone_number"] = cd["phone_number"]
            messages.success(request, self.success_message, "success")
            return redirect("accounts:user_register_verify")

        context = {"register_form": register_form}
        return render(request, self.template_name, context)


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = "accounts/registration/verify.html"
    success_message = _(
        "Your registration was successful. Welcome to the iranigram family")

    def get(self, request):
        phone_number = self.request.session["phone_number"]
        verify_form = self.form_class
        context = {
            "verify_form": verify_form,
            "phone_number": phone_number,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        phone_number = self.request.session["phone_number"]
        verify_form = self.form_class(request.POST, request=self.request)
        if verify_form.is_valid():
            user = User.objects.create_user(phone_number)
            # send_register_success_sms_task.delay(phone_number)
            login(request, user)
            messages.success(request, self.success_message, "success")
            return redirect("accounts:new_order")

        context = {
            "verify_form": verify_form,
            "phone_number": phone_number,
        }
        return render(request, self.template_name, context)


class UserLoginWithPassView(View):
    form_class = LoginWithPasswordForm
    template_name = "accounts/registration/login_with_pass.html"
    success_message = _("You have successfully logged into your account"),

    def get(self, request):
        login_form = self.form_class
        context = {"login_form": login_form}
        return render(request, self.template_name, context)

    def post(self, request):
        login_form = self.form_class(request.POST)
        if login_form.is_valid():
            try:
                cd = login_form.cleaned_data
                user = authenticate(
                    username=cd["phone_number"],
                    password=cd["password"],
                )
                if user is not None:
                    login(request, user)
                    messages.success(request, self.success_message, "success")
                    return redirect("accounts:user_dashboard")
            except ValidationError as e:
                logger.error(f"ValidationError in login view: {str(e)}")
        else:
            context = {"login_form": login_form}
            return render(request, self.template_name, context)


class UserLoginWithOTPView(View):
    form_class = LoginWithOTPForm
    template_name = "accounts/registration/login_with_otp.html"
    success_message = _("A one-time password has been sent")

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("pages:home")
        otp_login_form = self.form_class
        context = {"otp_login_form": otp_login_form}
        return render(request, self.template_name, context)

    def post(self, request):
        otp_login_form = self.form_class(request.POST)
        if otp_login_form.is_valid():
            cd = otp_login_form.cleaned_data
            phone_number = cd["phone_number"]
            request.session["phone_number"] = phone_number
            messages.success(request, self.success_message, "success")
            return redirect("accounts:user_login_verify")
        else:
            context = {"otp_login_form": otp_login_form}
            return render(request, self.template_name, context)


@csrf_exempt
def check_expire_time(request):
    phone_number = request.GET.get("phone_number")
    request.session["phone_number"] = phone_number
    try:
        remain_time = otp_manager.check_expire_time(phone_number)
        if remain_time is not None:
            return JsonResponse({"msg": "True", 'remain_time': remain_time})
        else:
            return JsonResponse({"msg": 'False', 'error': 'OTP not found or has expired'})

    except Exception as e:
        return JsonResponse({"msg": 'False', 'error': f'Error: {str(e)}'}, status=200)


@csrf_exempt
def send_otpcode_again(request):
    phone_number = request.GET.get("phone_number")
    otp_manager.login_with_otp(phone_number)
    messages.success(request, _("A one-time password has been sent"), "success")
    return JsonResponse({"status": True})


class UserLoginVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = "accounts/registration/verify.html"
    success_message = _("You have successfully logged into your account")

    def get(self, request):
        phone_number = self.request.session["phone_number"]
        if request.user.is_authenticated:
            return redirect("pages:home")
        verify_form = self.form_class
        context = {
            "verify_form": verify_form,
            "phone_number": phone_number,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        phone_number = self.request.session["phone_number"]
        verify_form = self.form_class(request.POST, request=self.request)
        if verify_form.is_valid():
            user = User.objects.get(phone_number=phone_number)
            if user is not None:
                login(request, user)
                messages.success(request, self.success_message, "success")
                return redirect("accounts:user_dashboard")

        context = {
            "verify_form": verify_form,
            "phone_number": phone_number,
        }
        return render(request, "accounts/registration/verify.html", context)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("pages:home")


class EditProfileFormView(BlockCheckLoginRequiredMixin, View):
    template_name = "accounts/profile.html"

    def get(self, request, *args, **kwargs):
        initial_info = {
            "full_name": request.user.full_name,
            "email": request.user.email,
        }
        profile_form = EditProfileForm(initial=initial_info)
        change_password_form = ChangePasswordForm()
        context = {
            "profile_form": profile_form,
            "change_password_form": change_password_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        profile_form = EditProfileForm(request.POST)
        change_password_form = ChangePasswordForm(request.POST)
        if "change_profile" in request.POST:
            if profile_form.is_valid():
                cd = profile_form.cleaned_data
                if cd["full_name"] == "":
                    cd["full_name"] = _("Guest User")
                user = request.user
                if cd["email"] is None or cd["email"] == '':
                    user.email = f'{request.user.phone_number}@iranigram.com'
                else:
                    user.email = cd["email"]
                user.full_name = cd["full_name"]
                user.save()
                messages.success(request, _("your profile updated"), "success")
                return redirect("accounts:user_profile")
            else:
                messages.error(request, _("There was an error with your profile form"), "danger")
                return redirect("accounts:user_profile")
        elif "change_password" in request.POST:
            if change_password_form.is_valid():
                cd = change_password_form.cleaned_data
                user = request.user
                user.set_password(cd["password2"])
                user.save()
                messages.success(request, _(
                    "Your password has been saved"), "success")
                return redirect("accounts:user_profile")
            else:
                messages.error(
                    request, 
                    _("There was an error with your password form"), 
                    "danger"
                )
                return redirect("accounts:user_profile")
        else:
            messages.error(request, _("Invalid request"), "danger")
            return redirect("accounts:user_profile")


class WalletView(BlockCheckLoginRequiredMixin, View):
    form_class = AddCreditForm
    template_name = "accounts/wallet.html"

    def get(self, request):
        add_credit_form = self.form_class
        context = {"add_credit_form": add_credit_form}
        return render(request, self.template_name, context)

    def post(self, request):
        add_credit_form = self.form_class(request.POST)
        if add_credit_form.is_valid():
            cd = add_credit_form.cleaned_data
            amount = int(cd["amount"])
            if amount < 500:
                messages.error(
                    request,
                    _("The minimum amount that can be paid to increase credit is 500 Tomans"),
                    "danger",
                )
                return redirect("accounts:user_wallet")
            phone_number = request.user.phone_number
            transaction_detail = (_("Increase wallet credit"),)
            request.session["transaction_detail"] = transaction_detail
            request.session["phone_number"] = phone_number
            request.session["amount_payable"] = amount
            request.session["payment_purpose"] = "add_fund_wallet"
            return redirect("payment_request")
        else:
            # print(add_credit_form.errors.as_data())  # TODO change this print to logging
            context = {"add_credit_form": add_credit_form}
            return render(request, self.template_name, context)


class ApiDocsView(View):
    template_name = 'accounts/api_docs.html'

    def get(self, request):
        user = request.user

        token = None
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        context = {
            'token': token,
            'site_url': settings.SITE_URL
        }

        return render(request, self.template_name, context)


def regenerate_token(request):
    user = request.user
    try:
        token = Token.objects.get(user=user)
        token.delete()
    except Token.DoesNotExist:
        pass

    Token.objects.create(user=user)
    messages.success(request, "Token has been replaced", "success")
    return redirect('accounts:api_docs')


class ServicesView(ListView):
    model = Service
    template_name = "accounts/services.html"
    context_object_name = "Services"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Service.objects.filter(available_for_user=True).order_by("priority")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context["object_list"], self.paginate_by)
        page = self.request.GET.get("page")

        try:
            services = paginator.page(page)
        except PageNotAnInteger:
            services = paginator.page(1)
        except EmptyPage:
            services = paginator.page(paginator.num_pages)
        context["Services"] = services
        return context
