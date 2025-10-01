from rest_framework import serializers
from .models import Badge

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'badge_type', 'earned_at']
