import json
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from users.renderers import APIJSONRenderer
from users.models import User
# from users.utilities.email import send_email_to_user


from users.serializers import (
    UserRegisterSerializer,
    LoginSerializer,
    UserSerializer,
)


class UserLoginAPIView(APIView):
    
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    # renderer_classes = APIJSONRenderer
    
    def post(self, request):
        user = {
            "email": request.data.get('email'),
            "password": request.data.get('password')
        }
        
        try:
            
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Http404:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        except ValidationError:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class UserRegisterAPIView(APIView):
    
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    # renderer_classes = APIJSONRenderer
    
    
    def post(self, request):
        user = {
            "email": request.data.get('email'),
            "username": request.data.get('email'),
            "password": request.data.get('password'),
            "role": request.data.get('role')
        }
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    