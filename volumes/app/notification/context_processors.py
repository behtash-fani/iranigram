from .models import Notification

def unread_notification_count(request):
    if request.user.is_authenticated:
        # Efficiently filter unread notifications
        unread_count = Notification.objects.filter(
            readers__isnull=True,  # Check for users NOT in the readers list
            is_active=True
        ).count()
    else:
        unread_count = 0
    return {'unread_notification_count': unread_count}