from django.db import models
from django.conf import settings

class Badge(models.Model):
    BADGE_TYPES = [
        ('first_deposit', 'First Deposit'),
        ('streak_7', '7 Day Streak'),
        ('streak_30', '30 Day Streak'),
        ('saving_milestone', 'Saving Milestone'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge_type')

    def __str__(self):
        return f"{self.user.email} - {self.badge_type}"
