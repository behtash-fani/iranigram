from support.views import ticket_detail, admin_ticket_detail
from orders.views import OrdersListView, PayView
from transactions.views import TransactionsView
from support.views import SubmitTicket
from support.views import SupportView
from notification.views import(
    DiscountNotificationView,
    OrdersNotificationView,
    ServicesNotificationView,
    GeneralNotificationView,
    make_notification_as_read
 )
from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('state/', views.UserDashboardView.as_view(), name='user_dashboard'),
    path('register', views.UserRegisterWithOTPView.as_view(), name='user_register'),
    path('verify-register/', views.UserRegisterVerifyCodeView.as_view(),name='user_register_verify'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('login-pass/', views.UserLoginWithPassView.as_view(),name='user_login_pass'),
    path('login-otp/', views.UserLoginWithOTPView.as_view(), name='user_login_otp'),
    path('verify-login/', views.UserLoginVerifyCodeView.as_view(),name='user_login_verify'),
    path('send-otpcode-again/', views.send_otpcode_again,name='send_otpcode_again'),
    path('new-order/', PayView.as_view(), name='new_order'),
    path('profile/', views.EditProfileFormView.as_view(), name='user_profile'),
    path('orders/', OrdersListView.as_view(), name='user_orders'),
    path('notification/discount/', DiscountNotificationView.as_view(), name='notices_discount'),
    path('notification/orders/', OrdersNotificationView.as_view(), name='notices_orders'),
    path('notification/servies/', ServicesNotificationView.as_view(), name='notices_services'),
    path('notification/general/', GeneralNotificationView.as_view(), name='notices_general'),
    path('make_as_read/<int:pk>/', make_notification_as_read, name='make_as_read'),
    path('wallet/', views.WalletView.as_view(), name='user_wallet'),
    path('transactions/', TransactionsView.as_view(), name='user_transactions'),
    path('api-docs/', views.ApiDocsView.as_view(), name='api_docs'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('regenerate-token/', views.regenerate_token, name='regenerate_token'),
    path('support/tickets', SupportView.as_view(), name='user_support'),
    path('support/new-ticket/', SubmitTicket.as_view(), name='submit_ticket'),
    path('support/<int:ticket_id>/', ticket_detail, name='ticket_detail'),
    path('admin/ticket/<int:ticket_id>/',admin_ticket_detail, name='admin_ticket_detail'),
    path('check-expire-time/', views.check_expire_time, name='check_expire_time'),
]
