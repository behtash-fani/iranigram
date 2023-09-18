from django.shortcuts import render
from django.views import View
from seo.models import PagesSeo
from posts.models import Post


class HomeView(View):
    template_name = "pages/home.html"

    def get(self, request):
        description_tag = PagesSeo.objects.filter(page='home')[0].description_tag
        keywords_tag = PagesSeo.objects.filter(page='home')[0].keywords_tag
        title_tag = PagesSeo.objects.filter(page='home')[0].title_tag
        canonical_link = PagesSeo.objects.filter(page='home')[0].canonical_link
        posts = Post.objects.all()[0:4]
        context = {
            'description_tag': description_tag,
            'keywords_tag': keywords_tag,
            'title_tag': title_tag,
            'canonical_link': canonical_link,
            'posts': posts
        }
        return render(request, self.template_name, context)


class FollowerView(View):
    template_name = "pages/buy_follower.html"

    def get(self, request):
        description_tag = PagesSeo.objects.filter(page='buy_follower')[0].description_tag
        keywords_tag = PagesSeo.objects.filter(page='buy_follower')[0].keywords_tag
        title_tag = PagesSeo.objects.filter(page='buy_follower')[0].title_tag
        context = {
            'description_tag': description_tag,
            'keywords_tag': keywords_tag,
            'title_tag': title_tag,
        }
        return render(request, self.template_name, context)


class LikeView(View):
    template_name = "pages/buy_like.html"

    def get(self, request):
        # meta_description_tag = PagesSeo.objects.filter(page='buy_like')[0].meta_description_tag
        title_tag = PagesSeo.objects.filter(page='buy_like')[0].title_tag
        context = {
            # 'meta_description_tag': meta_description_tag,
            'title_tag': title_tag,
        }
        return render(request, self.template_name, context)


class ViewView(View):
    template_name = "pages/buy_view.html"

    def get(self, request):
        # meta_description_tag = PagesSeo.objects.filter(page='buy_view')[0].meta_description_tag
        title_tag = PagesSeo.objects.filter(page='buy_view')[0].title_tag
        context = {
            # 'meta_description_tag': meta_description_tag,
            'title_tag': title_tag,
        }
        return render(request, self.template_name, context)
