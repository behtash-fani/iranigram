from .models import Service
from django.http import JsonResponse


def service_list(request):
    service_type_id = request.GET['serviceTypeId']
    services = list(Service.objects.filter(service_type__id=service_type_id, available_for_user=True).values())
    context = {'services': services}
    return JsonResponse(context)


def get_description(request):
    service_id = request.GET['serviceId']
    service_detail = list(Service.objects.filter(id=service_id).values())[0]
    context = {'service_detail': service_detail}
    return JsonResponse(context)
