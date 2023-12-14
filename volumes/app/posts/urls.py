from django.urls import path
from . import views



app_name = 'posts'
urlpatterns = [
    path('', views.PostsList.as_view(), name='posts_list'),
    path('<str:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
