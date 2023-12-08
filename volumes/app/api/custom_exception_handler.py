from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def auth_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is None:
        message = 'Authentication is required to access this resource.'
        return Response({'error': message}, status=status.HTTP_401_UNAUTHORIZED)
    
    if response.data["detail"].code == "not_authenticated":
        message = 'Authentication is required to access this resource.'
        return Response({'error': message}, status=status.HTTP_401_UNAUTHORIZED)
    
    if response.data["detail"].code == "authentication_failed":
        message = 'Authentication credentials were not provided.'
        return Response({'error': message}, status=status.HTTP_401_UNAUTHORIZED)