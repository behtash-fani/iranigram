from .models import Notification
from django.db.models import Count, Q

def unread_notification_count(request):
    unread_count = 0
    categories_counts = {}
    if request.user.is_authenticated:
        user = request.user
        active_filter = Q(is_active=True)
        unread_filter = ~Q(readers=user)

        # Count unread notifications for different categories
        categories_counts = {
            'discount': Notification.objects.filter(Q(category_id=4) & unread_filter & active_filter).count(),
            'orders': Notification.objects.filter(Q(user=user) & unread_filter & active_filter).count(),
            'services': Notification.objects.filter((Q(category_id=2) | Q(category_id=3)) & unread_filter & active_filter).count(),
            'general': Notification.objects.filter(Q(category_id=1) & unread_filter & active_filter).count(),
        }

        # Calculate total unread count
        unread_count = sum(categories_counts.values())
        return {
            'unread_notification_count': unread_count,
            'discount_count': categories_counts['discount'],
            'orders_count': categories_counts["orders"],
            'services_count': categories_counts["services"],
            'general_count': categories_counts["general"],
        }
    else:
        unread_count = 0
        return {
            'unread_notification_count': unread_count,
        }

    

