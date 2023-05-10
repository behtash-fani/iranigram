from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from orders.models import Order
from orders.forms import OrderForm, TemplateOrderForm
from accounts.forms import VerifyCodeForm
from service.models import Service, ServiceType
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
from accounts.models import User
from django.contrib.auth import authenticate, logout, login

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


class TempalateNewOrderView(View):
    template_name = "orders/buypage.html"

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            phone_number = request.user.phone_number
            temp_order_form = TemplateOrderForm(initial={'phone_number': phone_number})
            context = {
                "phone_number": phone_number,
            }
        else:
            temp_order_form = TemplateOrderForm
        verify_form = VerifyCodeForm
        quantity = kwargs.get("quantity")
        request.session["quantity"] = quantity
        service_id = kwargs.get("service_id")
        request.session["service_id"] = service_id
        service = Service.objects.get(id=service_id)
        price_per_unit_service = service.amount
        amount = int(quantity)*int(service.amount)
        context |= {
            "quantity": quantity,
            "service_id": service_id,
            'service' : service,
            'price_per_unit_service' : price_per_unit_service,
            "temp_order_form": temp_order_form,
            "verify_form": verify_form,
            "amount": amount,
            }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            phone_number = request.user.phone_number
        else:
            phone_number = self.request.session["phone_number"]
        service_id = kwargs.get("service_id")
        request.session["service_id"] = service_id
        verify_form = VerifyCodeForm(request.POST or None, request=self.request)
        temp_order_form = TemplateOrderForm(request.POST or None, request=request, initial={'phone_number': phone_number})
        if verify_form.is_valid() or temp_order_form.is_valid():
            service_id = self.request.session["service_id"]
            if request.user.is_authenticated:
                link = temp_order_form.cleaned_data["link"]
            else:
                link = self.request.session["link"]
            service = Service.objects.get(id=service_id)
            quantity = self.request.session["quantity"]
            if User.objects.filter(phone_number=phone_number).exists():
                user = User.objects.get(phone_number=phone_number)
            else:
                user = User.objects.create_user(phone_number)
            amount = int(quantity)*int(service.amount)
            if user is not None:
                login(request, user)
                order_code = generate_random_number(8, is_unique=True)
                order = Order.objects.create(
                    user = user,
                    service_type = service.service_type,
                    service = service,
                    order_code = order_code,
                    link = link,
                    quantity = quantity,
                    amount = amount,
                    online_paid_amount = amount,
                    payment_method = 'online',
                )
                transaction_detail = (_("Online payment of the order fee"),)
                request.session["phone_number"] = phone_number
                request.session["order_id"] = order.id
                request.session["amount"] = amount
                request.session["payment_type"] = "pay_order_online"
                request.session["transaction_detail"] = transaction_detail
                request.session["service_id"] = service_id
                return redirect("payment_request")
        else:
            context = {
                "verify_form": verify_form,
                "temp_order_form": temp_order_form,
                "phone_number": phone_number,
                "amount": amount,
                }
            return render(request, self.template_name, context)