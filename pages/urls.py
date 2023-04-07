from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('iranian-instagram-follower/', views.FollowerView.as_view(), name='follower'),
    path('iranian-instagram-like/', views.LikeView.as_view(), name='like'),
    path('iranian-instagram-view/', views.ViewView.as_view(), name='view'),

]
