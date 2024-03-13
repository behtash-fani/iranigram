from .models import Notification
from django.db.models import Q


def unread_notification_count(request):
    if request.user.is_authenticated:
        user_to_check = request.user
        unread_count = Notification.objects.filter(
            ~Q(readers=user_to_check), is_active=True).count()
    else:
        unread_count = 0
    return {'unread_notification_count': unread_count}
