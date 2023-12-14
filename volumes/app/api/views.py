from orders.models import Order
from .serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.models import Service
from common.generate_random_number import generate_random_number
from transactions.models import Transactions as Trans
from django.utils.translation import gettext as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle


class StatusOrderView(APIView):
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        order_code = request.data.get('order_code')
        if not order_code:
            return Response({'error': 'order code is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(user=request.user, order_code=order_code)
            context = {
                'order': order.order_code,
                'status': order.status,
                'balance': str(request.user.balance),
                'start_count': str(order.start_count),
                'remains': str(order.remains)
            }
            return Response(context, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found with this order code'}, status=status.HTTP_404_NOT_FOUND)


class AddOrderView(APIView):
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        service_code = request.data.get("service_code")
        link = request.data.get("link")
        quantity = request.data.get("quantity")
        user = request.user

        required_fields = ['service_code', 'link', 'quantity']

        for field in required_fields:
            if field not in request.data or not request.data[field]:
                return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            service = Service.objects.filter(service_code=service_code).first()
        except Service.DoesNotExist:
            return Response({'message': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

        if int(quantity) <= 0:
            return Response({'message': 'Quantity must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not int(service.min_order) <= int(quantity) <= int(service.max_order):
            return Response({'message': f'Quantity must be between {service.min_order} and {service.max_order}'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        total_price = int(service.amount) * int(quantity)
        if int(user.balance) < int(total_price):
            return Response({'message': 'Your balance is less than the order amount'}, status=status.HTTP_200_OK)

        #Create the order
        order_code = generate_random_number(8, is_unique=True)
        user.balance -= total_price
        user.save()
        order_item = Order.objects.create(
            user=user,
            service_type=service.service_type,
            service=service,
            order_code=order_code,
            link=link,
            quantity=quantity,
            amount=total_price,
            wallet_paid_amount=total_price,
            submit_order_method="api",
            payment_method="wallet",
            status='Queued',
            paid=True,
        )

        transaction_detail = _("Deduct the amount for placing the order")
        Trans.objects.create(
            user=user,
            type="payment_for_order",
            balance=user.balance,
            price=total_price,
            payment_type="wallet",
            order_code=order_item.order_code,
            details=transaction_detail,
            ip=request.META.get("REMOTE_ADDR"),
        )

        context = {
            'message': 'Order created successfully',
            'order_code': order_item.order_code
        }
        return Response(context, status=status.HTTP_201_CREATED)
        

class UserBalanceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            context = {
                'status': 'success',
                'balance': user.balance
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'An error occurred while fetching the balance'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)