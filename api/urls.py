from django.urls import path
from .views import *

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/token/refresh/', NewTokenRefreshView.as_view(), name='token_refresh'),
]
