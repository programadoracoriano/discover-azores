from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from .serializers import *

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
