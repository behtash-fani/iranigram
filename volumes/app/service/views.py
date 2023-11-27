from .models import Service
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


def service_list(request):
    service_type_id = request.GET['serviceTypeId']
    services = list(Service.objects.filter(service_type__id=service_type_id, available_for_user=True).order_by('priority').values())
    context = {'services': services}
    return JsonResponse(context)


def get_description(request):
    try:
        service_id = request.GET['serviceId']
        service_detail = list(Service.objects.filter(id=service_id).values())[0]
        context = {'service_detail': service_detail}
        return JsonResponse(context)
    except Exception as e:
        logger.error(f"An error occurred in get_description view: {e}")
        return JsonResponse({'error': str(e)}, status=500)
