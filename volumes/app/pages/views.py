from django.shortcuts import render
from django.views import View
from seo.models import PagesSeo

class HomeView(View):
    template_name = "pages/home.html"

    def get(self, request):
        meta_description_tag = PagesSeo.objects.filter(page='home')[0].meta_description_tag
        title_tag = PagesSeo.objects.filter(page='home')[0].title_tag
        context = {
            'meta_description_tag': meta_description_tag,
            'title_tag': title_tag,
            }
        return render(request, self.template_name, context)


class FollowerView(View):
    template_name = "pages/buy_follower.html"
    def get(self, request):
        meta_description_tag = PagesSeo.objects.filter(page='buy_follower')[0].meta_description_tag
        title_tag = PagesSeo.objects.filter(page='buy_follower')[0].title_tag
        context = {
            'meta_description_tag': meta_description_tag,
            'title_tag': title_tag,
            }
        return render(request, self.template_name, context)


class LikeView(View):
    template_name = "pages/buy_like.html"

    def get(self, request):
        return render(request, self.template_name)


class ViewView(View):
    template_name = "pages/buy_view.html"

    def get(self, request):
        return render(request, self.template_name)
