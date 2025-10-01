from django.db import models
from django.conf import settings

class SavingsJar(models.Model):
    PLAN_CHOICES = [
        ('base', 'Base'),
        ('premium', 'Premium'),
        ('advanced', 'Advanced'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES, default='base')
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    streak_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} - {self.plan_type} Jar"
