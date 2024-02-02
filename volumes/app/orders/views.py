from accounts.forms import LoginWithOTPForm, VerifyCodeForm
from accounts.mixins import BlockCheckLoginRequiredMixin
from orders.forms import OrderForm, TemplateNewOrderForm
from common.instagram.insta_info import InstagramAccInfo
from transactions.models import Transactions as Trans
from django.views.decorators.csrf import csrf_exempt
from orders.tasks import send_submit_order_sms_task
from django.core.paginator import PageNotAnInteger
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage
from django.core.paginator import Paginator
from django.views.generic import ListView
from common.otp_manager import OTPManager
from django.contrib.auth import login
from django.http import JsonResponse
from service.models import Packages
from django.contrib import messages
from accounts.models import User
from django.urls import reverse
from orders.models import Order
from django.views import View
import logging

otp_manager = OTPManager()
logger = logging.getLogger(__name__)


class CustomerMixin:
    def process_customer(self, request, order_form, use_wallet, submit_order_method, quantity=None, service=None, pkg_id=None):
        cd = order_form.cleaned_data
        user = request.user
        order_item = order_form.save(commit=False)
        order_code = otp_manager.generate_random_number(8, is_unique=True)
        if service is not None:
            order_item.service = service
            order_item.service_type = service.service_type
        if quantity is None:
            quantity = order_item.quantity
        unit_price = order_item.service.amount
        amount = int(unit_price) * int(quantity)
        order_item.quantity = quantity
        order_item.amount = amount
        order_item.user = user
        order_item.order_code = order_code
        order_item.submit_order_method = submit_order_method
        order_item.save()
        request.session["order_id"] = order_item.id
        request.session["phone_number"] = user.phone_number
        request.session["payment_purpose"] = "pay_order_online"
        request.session["amount_payable"] = amount
        if use_wallet:
            if user.balance >= amount:
                user.balance -= amount
                user.save()
                order_item.amount = amount
                order_item.wallet_paid_amount = amount
                order_item.online_paid_amount = 0
                order_item.save()
                status = finish_payment(
                    request, payment_method="wallet", trans_type="payment_for_order")
                if status:
                    messages.success(request, _(
                        "Order created successfully, this is your order code:") + f"{order_code}", "success",)
                    if pkg_id is not None:
                        return redirect(self.success_redirect_url, pkg_id)
                    return redirect(self.success_redirect_url)
            elif user.balance < amount:
                online_amount = amount - user.balance
                order_item.amount = amount
                order_item.wallet_paid_amount = user.balance
                order_item.online_paid_amount = online_amount
                order_item.save()
                if online_amount < 500:
                    online_amount = 500
                request.session["use_wallet_status"] = cd["use_wallet"]
                request.session["amount_payable"] = online_amount
                return redirect("payment_request")

        order_item.wallet_paid_amount = 0
        order_item.online_paid_amount = amount
        order_item.save()
        return redirect("payment_request")


class PayView(CustomerMixin, BlockCheckLoginRequiredMixin, View):
    template_name = "orders/new_order.html"
    form_class = OrderForm
    success_redirect_url = "accounts:new_order"
    failure_redirect_url = "accounts:new_order"

    def get(self, request):
        order_form = self.form_class
        context = {"order_form": order_form}
        return render(request, self.template_name, context)

    def post(self, request):
        order_form = self.form_class(request.POST or None)
        if order_form.is_valid():
            return self.process_customer(
                request, order_form, order_form.cleaned_data["use_wallet"], submit_order_method="panel")
        else:
            logger.error(order_form.errors.as_data())
            context = {"order_form": order_form}
            return render(request, self.template_name, context)


class TemplateNewOrder(CustomerMixin, View):
    template_name = "orders/buypage.html"
    form_class = TemplateNewOrderForm
    otp_form_class = LoginWithOTPForm
    verify_otp_form_class = VerifyCodeForm
    success_redirect_url = "orders:new_order"
    failure_redirect_url = "orders:new_order"

    def get(self, request, *args, **kwargs):
        pkg_id = kwargs["pkg_id"]
        pkg = Packages.objects.get(id=pkg_id)
        order_form = self.form_class
        otp_form = self.otp_form_class()
        verify_otp_form = self.verify_otp_form_class()
        context = {
            "order_form": order_form,
            'otp_form': otp_form,
            'verify_otp_form': verify_otp_form,
            "pkg": pkg
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pkg_id = kwargs["pkg_id"]
        pkg = Packages.objects.get(id=pkg_id)
        service = Packages.objects.get(id=pkg_id).service
        quantity = Packages.objects.get(id=pkg_id).quantity
        order_form = self.form_class(request.POST or None)
        otp_form = self.otp_form_class(request.POST or None)
        if order_form.is_valid():
            return self.process_customer(
                request, order_form,
                order_form.cleaned_data["use_wallet"],
                submit_order_method="packages",
                quantity=quantity,
                service=service,
                pkg_id=pkg_id
            )
        else:
            logger.error(order_form.errors.as_data())
            context = {
                "order_form": order_form,
                'otp_form': otp_form,
                "pkg": pkg
            }
            return render(request, self.template_name, context)


def finish_payment(request, payment_method=None, trans_type=None):
    user = request.user
    try:
        order_id = request.session["order_id"]
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.status = "Queued"
        order.payment_method = payment_method
        order.save()
        price, transaction_detail = 0, ""
        if payment_method == "wallet":
            price = order.wallet_paid_amount
            transaction_detail = _("Deduct the amount for placing the order")
        else:
            if order.online_paid_amount <= 500:
                price = 500
            else:
                price = order.online_paid_amount
            transaction_detail = _("Online payment of the order fee")
        send_submit_order_sms_task.delay(user.phone_number, order.order_code)
        Trans.objects.create(
            user=user,
            type=trans_type,
            balance=user.balance,
            price=price,
            payment_type=payment_method,
            order_code=order.order_code,
            details=transaction_detail,
            ip=request.META.get("REMOTE_ADDR"),
        )

    except Exception as e:
        logger.error(e)
        return False
    return True


@csrf_exempt
def complete_order(request):
    order_id = request.POST.get("order_id")
    order = Order.objects.get(id=order_id)
    amount = int(request.POST.get("amount"))
    print(amount)
    request.session["phone_number"] = request.user.phone_number
    request.session["total_order_price"] = order.amount
    request.session["amount_payable"] = amount
    request.session["order_id"] = order_id
    redirect_url = reverse("payment_request")
    return JsonResponse({"redirect": redirect_url})


class OrdersListView(BlockCheckLoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/orders.html"
    context_object_name = "Orders"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Order.objects.filter(
            user=self.request.user).order_by("-created_at")
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


def get_insta_info(request):
    link = request.GET["link"]
    service_link_type = request.GET["service_link_type"]
    account_info = InstagramAccInfo()
    if service_link_type == "instagram_post_link":
        username = account_info.get_username_from_link(link)
    else:
        username = link
        profile_acc_is_available = account_info.check_acc_is_available(
            username)
        if profile_acc_is_available:
            profile_pic_url = account_info.profile_pic_from_username(username)
            acc_privacy = account_info.acc_privacy(username)
            context = {
                "status": 'acc_available',
                "profile_pic": profile_pic_url,
                "acc_privacy": acc_privacy
            }
            return JsonResponse(context)
        else:
            context = {"status": 'acc_is_not_available'}
            return JsonResponse(context)


def get_phone_number(request):
    phone_number = request.GET["phone_number"]
    link = request.GET["link"]
    request.session["link"] = link
    request.session["phone_number"] = phone_number
    send_code_status = otp_manager.login_with_otp(phone_number)
    context = {'success': send_code_status, 'phone_number': phone_number}
    return JsonResponse(context)


def verify_phonenumber_pay(request):
    phone_number = request.GET["phone_number"]
    code = request.GET["otpCode"]
    verify_status = otp_manager.verify_otpcode(phone_number, code)
    if verify_status:
        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
            login(request, user)
        else:
            user = User.objects.create_user(phone_number)
            login(request, user)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def send_to_payment(request):
    pkg_id = request.GET.get('pkg-id')
    package = Packages.objects.get(id=pkg_id)
    service = package.service
    service_type = package.service.service_type
    order_code = otp_manager.generate_random_number(8, is_unique=True)
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
        quantity=quantity,
        amount=amount,
        wallet_paid_amount=0,
        online_paid_amount=amount,
        submit_order_method="packages",
        payment_method="online",
        status="Queued",
    )
    request.session["phone_number"] = phone_number
    request.session["order_id"] = order_item.id
    request.session["amount_payable"] = amount
    request.session["payment_purpose"] = "pay_order_online"
    return redirect("payment_request")
