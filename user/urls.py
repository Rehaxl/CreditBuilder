from django.urls import path
from .views import RegisterView, LoginView, ProfileView, KYCUploadView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('kyc-upload/', KYCUploadView.as_view(), name='kyc-upload'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
