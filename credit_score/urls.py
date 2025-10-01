from django.urls import path
from .views import CreditScoreView

urlpatterns = [
    path('credit-score/', CreditScoreView.as_view(), name='credit-score'),
]
