from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import CreditScore
from .serializers import CreditScoreSerializer

class CreditScoreView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        score, created = CreditScore.objects.get_or_create(user=user, defaults={'score': 0, 'predicted_score': 0})
        # Update score based on streak
        from savings_jar.models import SavingsJar
        total_streak = SavingsJar.objects.filter(user=user).aggregate(total_streak=models.Sum('streak_count'))['total_streak'] or 0
        score.score = total_streak * 10
        score.predicted_score = score.score + 50  # dummy
        score.save()
        serializer = CreditScoreSerializer(score)
        return Response(serializer.data)
