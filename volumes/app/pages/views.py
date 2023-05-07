from django.shortcuts import render
from django.views import View
from service.models import Service
import json 

class HomeView(View):
    template_name = "pages/home.html"

    def get(self, request):
        template_service = Service.objects.filter(template_service=True).order_by('priority')
        follower_services = Service.objects.filter(template_service=True, template_service_category='follower').order_by('priority')
        like_services = Service.objects.filter(template_service=True, template_service_category='like').order_by('priority')
        view_services = Service.objects.filter(template_service=True, template_service_category='view').order_by('priority')
        context = {
            'services' : template_service,
            'follower_services': follower_services,
            'like_services': like_services,
            'view_services': view_services,
        }
        return render(request, self.template_name, context)


class FollowerView(View):
    template_name = "pages/buy_follower.html"

    def get(self, request):
        template_service = Service.objects.filter(template_service=True).order_by('priority')
        follower_services = Service.objects.filter(template_service=True, template_service_category='follower').order_by('priority')
        context = {
            'services' : template_service,
            'follower_services': follower_services,
        }
        return render(request, self.template_name, context)


class LikeView(View):
    template_name = "pages/buy_like.html"

    def get(self, request):
        template_service = Service.objects.filter(template_service=True).order_by('priority')
        like_services = Service.objects.filter(template_service=True, template_service_category='like').order_by('priority')
        context = {
            'services' : template_service,
            'like_services': like_services,
        }
        return render(request, self.template_name, context)


class ViewView(View):
    template_name = "pages/buy_view.html"

    def get(self, request):
        template_service = Service.objects.filter(template_service=True).order_by('priority')
        view_services = Service.objects.filter(template_service=True, template_service_category='view').order_by('priority')
        context = {
            'services' : template_service,
            'view_services': view_services,
        }
        return render(request, self.template_name, context)
