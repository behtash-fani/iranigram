from django.urls import path
from . import views



app_name = 'comments'
urlpatterns = [
    path("list", views.submit_comment, name='comments_list')
]