from .models import Post
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import DetailView
from comments.models import Comment




class PostsList(ListView):
    model = Post
    template_name = 'posts/posts_list.html'
    context_object_name = 'Posts'
    context_object_name = 'slider_posts'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        posts = Post.objects.filter(status="publish")[4:]
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginate_by)
        posts = Post.objects.all()
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['Posts'] = posts
        context["slider_posts"] = Post.objects.filter(status="publish")[:4]
        return context



class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/post_detail.html'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Posts'] = Post.objects.all()
        slug = self.kwargs['slug']
        post_id = Post.objects.filter(slug=slug).first().id
        context["comments"] = Comment.objects.filter(status= 'approved', page_id=post_id)
        context["page_id"] = post_id
        return context