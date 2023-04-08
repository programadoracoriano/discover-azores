from django.urls import path
from .views import *
from rest_framework_simplejwt.views import jwt_refresh_view
urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/token/refresh/', jwt_refresh_view.as_view(), name='token_refresh'),
]
