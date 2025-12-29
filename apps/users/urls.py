from django.urls import path
from .views import UserRegisterView, UserMeView, EmailTokenObtainPairView, UserLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('token/', EmailTokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]