from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from seo.models import PagesSeo
from posts.models import Post
from service.models import Packages
from comments.models import Comment, Response


def handling_404(request, exception):
    return render(request, 'pages/404.html', {})


class HomeView(View):
    template_name = "pages/home.html"

    def get(self, request):
        description_tag = PagesSeo.objects.filter(page='home')[
            0].description_tag
        keywords_tag = PagesSeo.objects.filter(page='home')[0].keywords_tag
        title_tag = PagesSeo.objects.filter(page='home')[0].title_tag
        canonical_link = PagesSeo.objects.filter(page='home')[0].canonical_link
        flw_service_tags = ['flw1', 'flw2', 'flw3']
        flw_packages = {}
        for tag in flw_service_tags:
            packages = Packages.objects.filter(
                service__available_for_package=True,
                service__service_tag=tag,
                enable=True
            ).order_by('priority')
            flw_packages[tag] = packages

        like_service_tags = ['like1', 'like2', 'like3']
        like_packages = {}
        for tag in like_service_tags:
            packages = Packages.objects.filter(
                service__available_for_package=True,
                service__service_tag=tag,
                enable=True
            ).order_by('priority')
            like_packages[tag] = packages

        view_service_tags = ['view1', 'view2', 'sview']
        view_packages = {}
        for tag in view_service_tags:
            packages = Packages.objects.filter(
                service__available_for_package=True,
                service__service_tag=tag,
                enable=True
            ).order_by('priority')
            view_packages[tag] = packages
        posts = Post.objects.all()[0:4]
        comments = Comment.objects.filter(
            page_id="home", status="approved").order_by('-created_at')

        context = {
            'description_tag': description_tag,
            'keywords_tag': keywords_tag,
            'title_tag': title_tag,
            'canonical_link': canonical_link,
            'flw_packages': flw_packages,
            'like_packages': like_packages,
            'view_packages': view_packages,
            'posts': posts,
            'comments': comments,
            'page_id': 'home'
        }
        return render(request, self.template_name, context)


class FollowerView(View):
    template_name = "pages/buy_follower.html"

    def get(self, request):
        # SEO tags
        description_tag = PagesSeo.objects.filter(
            page='buy_follower')[0].description_tag
        keywords_tag = PagesSeo.objects.filter(
            page='buy_follower')[0].keywords_tag
        title_tag = PagesSeo.objects.filter(page='buy_follower')[0].title_tag
        canonical_link = PagesSeo.objects.filter(
            page='buy_follower')[0].canonical_link

        # Followers Packages
        flw_service_tags = ['flw1', 'flw2', 'flw3']
        flw_packages = {}
        for tag in flw_service_tags:
            packages = Packages.objects.filter(
                service__available_for_package=True,
                service__service_tag=tag,
                enable=True
            ).order_by('priority')
            flw_packages[tag] = packages
        comments = Comment.objects.filter(
            page_id="follower", status="approved").order_by('-created_at')

        context = {
            'description_tag': description_tag,
            'keywords_tag': keywords_tag,
            'title_tag': title_tag,
            'canonical_link': canonical_link,
            'title_tag': title_tag,
            'flw_packages': flw_packages,
            'comments': comments,
            'page_id': 'follower'
        }
        return render(request, self.template_name, context)


class LikeView(View):
    template_name = "pages/buy_like.html"

    def get(self, request):
        description_tag = PagesSeo.objects.filter(page='buy_like')[
            0].description_tag
        keywords_tag = PagesSeo.objects.filter(page='buy_like')[0].keywords_tag
        title_tag = PagesSeo.objects.filter(page='buy_like')[0].title_tag
        canonical_link = PagesSeo.objects.filter(page='buy_like')[
            0].canonical_link
        like_service_tags = ['like1', 'like2', 'like3']
        like_packages = {}
        for tag in like_service_tags:
            packages = Packages.objects.filter(
                service__available_for_package=True,
                service__service_tag=tag,
                enable=True
            ).order_by('priority')
            like_packages[tag] = packages
        comments = Comment.objects.filter(page_id="like", status="approved")

        context = {
            'description_tag': description_tag,
            'keywords_tag': keywords_tag,
            'title_tag': title_tag,
            'canonical_link': canonical_link,
            'like_packages': like_packages,
            'comments': comments,
            'page_id': 'like'
        }
        return render(request, self.template_name, context)


class ViewView(View):
    template_name = "pages/buy_view.html"

    def get(self, request):
        description_tag = PagesSeo.objects.filter(page='buy_view')[
            0].description_tag
        keywords_tag = PagesSeo.objects.filter(page='buy_view')[0].keywords_tag
        title_tag = PagesSeo.objects.filter(page='buy_view')[0].title_tag
        canonical_link = PagesSeo.objects.filter(page='buy_view')[
            0].canonical_link

        view_service_tags = ['view1', 'view2', 'sview']
        view_packages = {}
        for tag in view_service_tags:
            packages = Packages.objects.filter(
                service__available_for_package=True,
                service__service_tag=tag,
                enable=True
            ).order_by('priority')
            view_packages[tag] = packages
        comments = Comment.objects.filter(
            page_id="view", status="approved").order_by('-created_at')

        context = {
            'description_tag': description_tag,
            'keywords_tag': keywords_tag,
            'title_tag': title_tag,
            'canonical_link': canonical_link,
            'view_packages': view_packages,
            'comments': comments,
            'page_id': 'view'
        }
        return render(request, self.template_name, context)
