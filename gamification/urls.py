from django.urls import path
from .views import StreakView, BadgeListView

urlpatterns = [
    path('streaks/', StreakView.as_view(), name='streaks'),
    path('badges/', BadgeListView.as_view(), name='badges'),
]
