from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Badge
from savings_jar.models import SavingsJar

@shared_task
def update_daily_streaks():
    # Reset streaks if no deposit in last 24 hours
    yesterday = timezone.now() - timedelta(days=1)
    jars = SavingsJar.objects.filter(last_deposit__lt=yesterday)
    for jar in jars:
        jar.streak_count = 0
        jar.save()
    return f"Updated streaks for {jars.count()} jars"

@shared_task
def award_badges():
    # Example: Award streak badges
    users_with_streak_7 = SavingsJar.objects.filter(streak_count__gte=7).values_list('user', flat=True).distinct()
    for user_id in users_with_streak_7:
        Badge.objects.get_or_create(user_id=user_id, badge_type='streak_7')
    # Similarly for others
    return f"Awarded badges to {len(users_with_streak_7)} users"
