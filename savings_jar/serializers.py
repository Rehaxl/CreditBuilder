from rest_framework import serializers
from .models import SavingsJar

class SavingsJarSerializer(serializers.ModelSerializer):
    plan_type = serializers.ChoiceField(choices=[('Base', 'Base'), ('Premium', 'Premium'), ('Advanced', 'Advanced')])

    class Meta:
        model = SavingsJar
        fields = ['id', 'plan_type', 'target_amount', 'current_amount', 'start_date', 'end_date', 'streak_count']
        read_only_fields = ['user', 'current_amount', 'streak_count']

class DepositSerializer(serializers.Serializer):
    jar_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)

class WithdrawSerializer(serializers.Serializer):
    jar_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
