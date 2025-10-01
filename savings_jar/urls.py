from django.urls import path
from .views import SavingsJarListCreateView, SavingsJarDetailView, DepositView, WithdrawView

urlpatterns = [
    path('', SavingsJarListCreateView.as_view(), name='jar-list-create'),
    path('<int:pk>/', SavingsJarDetailView.as_view(), name='jar-detail'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
]
