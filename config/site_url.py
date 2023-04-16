from django.conf import settings



def site_url(request):
    return {'site_url': settings.DJANGO_SITE_URL}