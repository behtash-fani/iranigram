from django.urls import path
from . import views
from support.views import submit_ticket, ticket_detail, admin_ticket_detail
from transactions.views import TransactionsView
from orders.views import OrdersListView, NewOrderView
from support.views import SupportView

app_name = 'accounts'

urlpatterns = [
    path('', views.UserDashboardView.as_view(), name='user_dashboard'),
    path('register/', views.UserRegisterWithOTPView.as_view(), name='user_register'),
    path('verify-register/', views.UserRegisterVerifyCodeView.as_view(),name='user_register_verify'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('login-pass/', views.UserLoginWithPassView.as_view(),name='user_login_pass'),
    path('login-otp/', views.UserLoginWithOTPView.as_view(), name='user_login_otp'),
    path('verify-login/', views.UserLoginVerifyCodeView.as_view(),name='user_login_verify'),
    path('send-otpcode-again/', views.send_otpcode_again,name='send_otpcode_again'),
    path('new-order/', NewOrderView.as_view(), name='new_order'),
    path('profile/', views.EditProfileFormView.as_view(), name='user_profile'),
    path('orders/', OrdersListView.as_view(), name='user_orders'),
    path('wallet/', views.WalletView.as_view(), name='user_wallet'),
    path('transactions/', TransactionsView.as_view(), name='user_transactions'),
    path('support/', SupportView.as_view(), name='user_support'),
    path('submit-ticket/', submit_ticket, name='submit_ticket'),
    path('ticket/<int:ticket_id>/', ticket_detail, name='ticket_detail'),
    path('admin/ticket/<int:ticket_id>/',admin_ticket_detail, name='admin_ticket_detail'),
    path('check-expire-time/', views.check_expire_time, name='check_expire_time'),
    # path('login/', views.login_with_otp_code, name='login_with_otp_code'),
]
