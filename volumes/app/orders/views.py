from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from orders.models import Order
from orders.forms import OrderForm, TemplateNewOrderForm
from service.models import Packages, Service, ServiceType
from django.views.generic import ListView
from transactions.models import Transactions as Trans
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import logging
from common.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from common.generate_random_number import generate_random_number
from django.views.decorators.csrf import csrf_exempt
from common.instagram.insta_info import InstagramAccInfo
from accounts.forms import LoginWithOTPForm, VerifyCodeForm
from accounts.tasks import send_login_sms_task
from datetime import datetime, timedelta
from accounts.models import OTPCode, User
from django.contrib.auth import login

logger = logging.getLogger("django")

class NewOrderView(LoginRequiredMixin, View):
    template_name = "orders/new_order.html"
    form_class = OrderForm

    def get(self, request):
        order_form = self.form_class
        context = {"order_form": order_form}
        return render(request, self.template_name, context)

    def post(self, request):
        order_form = self.form_class(request.POST or None)
        if order_form.is_valid():
            if "online_payment" in request.POST:
                cd = order_form.cleaned_data
                order_item = order_form.save(commit=False)
                order_code = generate_random_number(8, is_unique=True)
                user = request.user
                order_item.user = user
                order_item.order_code = order_code
                unit_price = Service.objects.get(id=cd["service"].id).amount
                total_price = int(unit_price) * int(cd["quantity"])
                if total_price < 500:
                    messages.error(
                        request,
                        _("For amounts less than 500 Tomans, please use a wallet"),
                        "danger",
                    )
                    return redirect("accounts:new_order")
                order_item.amount = total_price
                order_item.payment_method = "online"
                order_item.save()
                transaction_detail = (_("Online payment of the order fee"),)
                request.session["phone_number"] = user.phone_number
                request.session["order_id"] = order_item.id
                request.session["amount"] = total_price
                request.session["payment_type"] = "pay_order_online"
                request.session["transaction_detail"] = transaction_detail
                return redirect("payment_request")
            elif "credit_payment" in request.POST:
                cd = order_form.cleaned_data
                user = request.user
                order_item = order_form.save(commit=False)
                order_item.user = user
                order_item.order_code = generate_random_number(8, is_unique=True)
                unit_price = Service.objects.get(id=cd["service"].id).amount
                total_price = int(unit_price) * int(cd["quantity"])
                order_item.amount = total_price
                if user.balance > total_price:
                    user.balance -= total_price
                    user.save()
                    order_item.payment_method = "wallet"
                    order_item.status = "Queued"
                    order_item.wallet_paid_amount = total_price
                    order_item.paid = True
                    order_item.save()
                    transaction_detail = _("Deduct the amount for placing the order")
                    Trans.objects.create(
                        user=user,
                        type="payment_for_order",
                        balance=user.balance,
                        price=total_price,
                        payment_type="wallet",
                        order_code=order_item.order_code,
                        details=transaction_detail,
                        ip=request.META.get("REMOTE_ADDR"),
                    )
                    messages.success(
                        request,
                        _("Order created successfully, this is your order code:")
                        + f"{order_item.order_code}",
                        "success",
                    )
                    return redirect("accounts:new_order")
                else:
                    messages.error(
                        request,
                        _(
                            "Your balance amount is less than the order amount. Please use online payment"
                        ),
                        "warning",
                    )
                    return redirect("accounts:new_order")
        else:
            logger.error(order_form.errors.as_data())
            context = {"order_form": order_form}
            return render(request, self.template_name, context)


def pay_remain_price(request):
    service_type_id = request.POST.get("service_type")
    service_type = ServiceType.objects.get(id=service_type_id)
    service_id = request.POST.get("service")
    service = Service.objects.get(id=service_id)
    link = request.POST.get("link")
    order_quantity = request.POST.get("order_quantity")
    amount = int(request.POST.get("remain_price"))
    order_code = generate_random_number(8, is_unique=True)
    total_price = int(order_quantity) * int(service.amount)
    user = request.user
    order = Order.objects.create(
        user=user,
        service_type=service_type,
        service=service,
        order_code=order_code,
        link=link,
        quantity=order_quantity,
        amount=amount,
    )
    request.session["phone_number"] = user.phone_number
    request.session["total_order_price"] = total_price
    request.session["amount"] = amount
    request.session["payment_type"] = "pay_remain_price"
    request.session["order_id"] = order.id
    transaction_detail = (_("Payment of the order deficit"),)
    request.session["transaction_detail"] = transaction_detail
    redirect_url = reverse("payment_request")
    return JsonResponse({"redirect": redirect_url})


@csrf_exempt
def complete_order(request):
    order_id = request.POST.get("order_id")
    order = Order.objects.get(id=order_id)
    amount = int(request.POST.get("remain_price"))
    user = request.user
    request.session["phone_number"] = user.phone_number
    request.session["total_order_price"] = order.amount
    request.session["amount"] = amount
    request.session["payment_type"] = "pay_remain_price"
    request.session["order_id"] = order_id
    transaction_detail = (_("Online payment of the order fee"),)
    request.session["transaction_detail"] = transaction_detail
    redirect_url = reverse("payment_request")
    return JsonResponse({"redirect": redirect_url})


class OrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/orders.html"
    context_object_name = "Orders"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Order.objects.filter(user=self.request.user).order_by("-created_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context["object_list"], self.paginate_by)
        page = self.request.GET.get("page")

        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)
        context["Orders"] = orders
        return context


class TemplateNewOrder(View):
    template_name = "orders/buypage.html"
    form_class = TemplateNewOrderForm
    otp_form_class = LoginWithOTPForm
    verify_otp_form_class = VerifyCodeForm

    def get(self, request, *args, **kwargs):
        pkg_id = kwargs["pkg_id"]
        pkg = Packages.objects.get(id=pkg_id)
        order_form = self.form_class
        otp_form = self.otp_form_class()
        verify_otp_form = self.verify_otp_form_class()
        context = {
            "order_form": order_form,
            'otp_form': otp_form,
            'verify_otp_form':verify_otp_form,
            "pkg": pkg
            }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pkg_id = kwargs["pkg_id"]
        pkg = Packages.objects.get(id=pkg_id)
        service = Packages.objects.get(id=pkg_id).service
        service_type = service.service_type
        quantity = Packages.objects.get(id=pkg_id).quantity
        order_form = self.form_class(request.POST or None)
        otp_form = self.otp_form_class(request.POST or None)
        verify_otp_form = self.verify_otp_form_class(request.POST or None)
        if order_form.is_valid():
            if "online_payment" in request.POST:
                cd = order_form.cleaned_data
                order_item = order_form.save(commit=False)
                order_code = generate_random_number(8, is_unique=True)
                user = request.user
                order_item.user = user
                order_item.order_code = order_code
                order_item.quantity = quantity
                order_item.service = service
                order_item.service_type = service_type
                order_item.save()
                unit_price = Service.objects.get(id=service.id).amount
                total_price = int(unit_price) * int(pkg.quantity)
                order_item.amount = total_price
                order_item.payment_method = "online"
                order_item.save()
                transaction_detail = (_("Online payment of the order fee"),)
                request.session["phone_number"] = user.phone_number
                request.session["order_id"] = order_item.id
                request.session["amount"] = total_price
                request.session["payment_type"] = "pay_order_online"
                request.session["transaction_detail"] = transaction_detail
                return redirect("payment_request")
            elif "credit_payment" in request.POST:
                cd = order_form.cleaned_data
                user = request.user
                order_item = order_form.save(commit=False)
                order_item.user = user
                order_item.order_code = generate_random_number(8, is_unique=True)
                unit_price = Service.objects.get(id=service.id).amount
                total_price = int(unit_price) * int(pkg.quantity)
                order_item.amount = total_price
                if user.balance > total_price:
                    user.balance -= total_price
                    user.save()
                    order_item.payment_method = "wallet"
                    order_item.status = "Queued"
                    order_item.quantity = quantity
                    order_item.service = service
                    order_item.service_type = service_type
                    order_item.wallet_paid_amount = total_price
                    order_item.paid = True
                    order_item.save()
                    transaction_detail = _("Deduct the amount for placing the order")
                    Trans.objects.create(
                        user=user,
                        type="payment_for_order",
                        balance=user.balance,
                        price=total_price,
                        payment_type="wallet",
                        order_code=order_item.order_code,
                        details=transaction_detail,
                        ip=request.META.get("REMOTE_ADDR"),
                    )
                    messages.success(
                        request,
                        _("Order created successfully, this is your order code:")
                        + f"{order_item.order_code}",
                        "success",
                    )
                    return redirect("orders:new_order", pkg.id)
                else:
                    messages.error(
                        request,
                        _(
                            "Your balance amount is less than the order amount. Please use online payment"
                        ),
                        "warning",
                    )
                    return redirect("orders:new_order", pkg.id)
        else:
            context = {"order_form": order_form,'otp_form': otp_form, "pkg": pkg}
            return render(request, self.template_name, context)


def get_insta_info(request):
    link = request.GET["link"]
    service_link_type = request.GET["service_link_type"]
    account_info = InstagramAccInfo()
    if service_link_type == "instagram_post_link":
        username = account_info.get_username_from_link(link)
    else:
        username = link
        profile_acc_is_available = account_info.check_acc_is_available(username)
        if profile_acc_is_available:
            profile_pic_url = account_info.profile_pic_from_username(username)
            acc_privacy = account_info.acc_privacy(username)
            context = {"status": 'acc_available', "profile_pic": profile_pic_url, "acc_privacy": acc_privacy}
            return JsonResponse(context)
        else:
            context = {"status": 'acc_is_not_available'}
            return JsonResponse(context)
    
def get_phone_number(request):
    phone_number = request.GET["phone_number"]
    link = request.GET["link"]
    request.session["link"] = link
    request.session["phone_number"] = phone_number
    verification_code = generate_random_number(4, is_unique=False)
    send_login_sms_task.delay(phone_number, verification_code)
    if OTPCode.objects.filter(phone_number=phone_number).exists():
        OTPCode.objects.filter(phone_number=phone_number).delete()
    OTPCode.objects.create(
            phone_number=phone_number,
            code=verification_code,
            expire_time=datetime.now() + timedelta(seconds=120),
        )
    context = {'success': True, 'phone_number': phone_number}
    return JsonResponse(context)

def verify_phonenumber_pay(request):
    phone_number = request.GET["phone_number"]
    otp_code = request.GET["otpCode"]
    verification_code = OTPCode.objects.get(phone_number=phone_number)
    if int(otp_code) == int(verification_code.code):
            verification_code.delete()
            if User.objects.filter(phone_number=phone_number).exists():
                user = User.objects.get(phone_number=phone_number)
                login(request, user)
            else:
                user = User.objects.create_user(phone_number)
                login(request, user)
            return JsonResponse({'success': True, 'alert': "شماره موبایل شما تایید شد. در حال ارسال به درگاه بانکی ..."})
    context = {'success': True, 'otp_code': otp_code, 'phone_number': phone_number}
    return JsonResponse(context)


def send_to_payment(request):
    pkg_id = request.GET.get('pkg-id')
    package = Packages.objects.get(id=pkg_id)
    service = package.service
    service_type = package.service.service_type
    order_code = generate_random_number(8, is_unique=True)
    link = request.session['link']
    phone_number = request.session['phone_number']
    quantity = package.quantity
    amount = package.amount
    order_item = Order.objects.create(
        user=request.user,
        service_type=service_type,
        service=service,
        order_code=order_code,
        link=link,
        quantity = quantity,
        amount = amount,
        online_paid_amount = amount,
        payment_method = "online",
        status = "Queued",
        )
    transaction_detail = (_("Online payment of the order fee"),)
    request.session["phone_number"] = phone_number
    request.session["order_id"] = order_item.id
    request.session["amount"] = amount
    request.session["payment_type"] = "pay_order_online"
    request.session["transaction_detail"] = transaction_detail
    return redirect("payment_request")