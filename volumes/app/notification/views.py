from django.shortcuts import get_object_or_404, redirect, render
from .models import Notification
from django.views.generic import ListView
from django.core.paginator import EmptyPage
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger

class NotificationListView(ListView):
    model = Notification
    template_name = "notification/notices.html"
    context_object_name = "Notices"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Notification.objects.filter(is_active=True).order_by("-created_at")
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

def make_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    user = request.user
    notification.readers.add(user)
    return redirect('accounts:notification_list')