from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('iranian-instagram-followers/', views.FollowerView.as_view(), name='follower'),
    path('iranian_instagram_like/', views.LikeView.as_view(), name='like'),
    path('خرید-بازدید-ایرانی-اینستاگرام/', views.ViewView.as_view(), name='view'),
]