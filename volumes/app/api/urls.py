from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.StatusOrderView.as_view()),
    path('add/', views.AddOrderView.as_view()),
    path('balance/', views.UserBalanceView.as_view())
]