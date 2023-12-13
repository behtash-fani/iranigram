from django.urls import path
from . import views

app_name = 'services'
urlpatterns = [
    path('list/', views.service_list, name='service_list'),
    path('service/desc/', views.get_description, name='service_desc'),
]
