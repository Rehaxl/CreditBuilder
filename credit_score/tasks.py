from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from .models import CreditScore
from savings_jar.models import SavingsJar

@shared_task
def calculate_credit_score(user_id):
    user_jars = SavingsJar.objects.filter(user_id=user_id)
    total_streaks = sum(jar.streak_count for jar in user_jars)
    score = min(100, total_streaks * 10)  # Simple rule-based scoring
    CreditScore.objects.update_or_create(
        user_id=user_id,
        defaults={'score': score, 'last_updated': timezone.now()}
    )
    cache.set(f"user:{user_id}:score", score, timeout=3600)
    return f"Calculated score {score} for user {user_id}"

@shared_task
def batch_calculate_scores():
    users = SavingsJar.objects.values_list('user', flat=True).distinct()
    for user_id in users:
        calculate_credit_score.delay(user_id)
    return f"Queued score calculations for {len(users)} users"
