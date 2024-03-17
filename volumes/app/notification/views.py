from django.shortcuts import get_object_or_404, redirect
from .models import Notification
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


class DiscountNotificationView(ListView):
    model = Notification
    template_name = "notification/notices_discount.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(category__id=4, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notices_discount = Notification.objects.filter(category__id=4, is_active=True).order_by("-created_at")
        paginator_discount = Paginator(notices_discount, self.paginate_by)
        page_number = self.request.GET.get('page')

        try:
            notices_discount = paginator_discount.page(page_number)
        except PageNotAnInteger:
            notices_discount = paginator_discount.page(1)
        except EmptyPage:
            notices_discount = paginator_discount.page(paginator_discount.num_pages)

        context["notices_orders"] = notices_discount
        return context


class OrdersNotificationView(ListView):
    model = Notification
    template_name = "notification/notices_orders.html"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(Q(user=user) & Q(is_active=True))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notices_orders = Notification.objects.filter(
            user=self.request.user, is_active=True).order_by("-created_at")
        # user = self.request.user
        # context['notices_orders_count'] = Notification.objects.filter(Q(user=user) & ~Q(readers=user) & Q(is_active=True)).count()
        paginator_orders = Paginator(notices_orders, self.paginate_by)
        page_number = self.request.GET.get('page')

        try:
            notices_orders = paginator_orders.page(page_number)
        except PageNotAnInteger:
            notices_orders = paginator_orders.page(1)
        except EmptyPage:
            notices_orders = paginator_orders.page(paginator_orders.num_pages)

        context["notices_orders"] = notices_orders
        return context


class ServicesNotificationView(ListView):
    model = Notification
    template_name = "notification/notices_services.html"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter((Q(category__id=2) | Q(category__id=3)) & Q(is_active=True))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notices_services = Notification.objects.filter(
            (Q(category__id=2) | Q(category__id=3)) & Q(is_active=True)).order_by("-created_at")
        paginator_services = Paginator(notices_services, self.paginate_by)
        page_number = self.request.GET.get('page')

        try:
            notices_services = paginator_services.page(page_number)
        except PageNotAnInteger:
            notices_services = paginator_services.page(1)
        except EmptyPage:
            notices_services = paginator_services.page(
                paginator_services.num_pages)

        context["notices_services"] = notices_services
        return context


class GeneralNotificationView(ListView):
    model = Notification
    template_name = "notification/notices_general.html"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(category__id=1, is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notices_general = Notification.objects.filter(category__id=1, is_active=True).order_by("-created_at")
        paginator_general = Paginator(notices_general, self.paginate_by)
        page_number = self.request.GET.get('page')

        try:
            notices_general = paginator_general.page(page_number)
        except PageNotAnInteger:
            notices_general = paginator_general.page(1)
        except EmptyPage:
            notices_general = paginator_general.page(
                paginator_general.num_pages)

        context["notices_general"] = notices_general
        return context


def make_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    user = request.user
    notification.readers.add(user)
    return redirect(request.META.get('HTTP_REFERER', '/'))
