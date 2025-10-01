from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Badge
from .serializers import BadgeSerializer
from savings_jar.models import SavingsJar

class StreakView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        jars = SavingsJar.objects.filter(user=user)
        total_streak = sum(jar.streak_count for jar in jars)
        return Response({'current_streak': total_streak})

class BadgeListView(generics.ListAPIView):
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Badge.objects.filter(user=self.request.user)
