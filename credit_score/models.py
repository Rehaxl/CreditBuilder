from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CreditScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    predicted_score = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.score}"
