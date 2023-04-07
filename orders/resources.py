from import_export import resources
from .models import Order


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        skip_unchanged = True
        report_skipped = False
        dry_run = True