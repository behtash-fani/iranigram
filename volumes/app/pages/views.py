from django.shortcuts import render
from django.views import View


class HomeView(View):
    template_name = "pages/home.html"

    def get(self, request):
        return render(request, self.template_name)


class FollowerView(View):
    template_name = "pages/buy_follower.html"

    def get(self, request):
        return render(request, self.template_name)


class LikeView(View):
    template_name = "pages/buy_like.html"

    def get(self, request):
        return render(request, self.template_name)


class ViewView(View):
    template_name = "pages/buy_view.html"

    def get(self, request):
        return render(request, self.template_name)
