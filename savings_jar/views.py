from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.cache import cache
from .models import SavingsJar
from .serializers import SavingsJarSerializer, DepositSerializer, WithdrawSerializer
from transactions.models import Transaction

class SavingsJarListCreateView(generics.ListCreateAPIView):
    serializer_class = SavingsJarSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return SavingsJar.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SavingsJarDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SavingsJarSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return SavingsJar.objects.filter(user=self.request.user)

class DepositView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            jar_id = serializer.validated_data['jar_id']
            amount = serializer.validated_data['amount']
            try:
                jar = SavingsJar.objects.get(id=jar_id, user=request.user)
            except SavingsJar.DoesNotExist:
                return Response({'error': 'Jar not found'}, status=status.HTTP_404_NOT_FOUND)

            jar.current_amount += amount
            jar.streak_count += 1
            jar.save()

            # Record transaction
            Transaction.objects.create(user=request.user, jar=jar, transaction_type='deposit', amount=amount)

            # Update streak in Redis
            cache.set(f"user:{request.user.id}:streak", jar.streak_count)

            return Response(SavingsJarSerializer(jar).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WithdrawView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = WithdrawSerializer(data=request.data)
        if serializer.is_valid():
            jar_id = serializer.validated_data['jar_id']
            amount = serializer.validated_data['amount']
            try:
                jar = SavingsJar.objects.get(id=jar_id, user=request.user)
            except SavingsJar.DoesNotExist:
                return Response({'error': 'Jar not found'}, status=status.HTTP_404_NOT_FOUND)

            if jar.current_amount >= amount:
                jar.current_amount -= amount
                jar.save()

                # Record transaction
                Transaction.objects.create(user=request.user, jar=jar, transaction_type='withdraw', amount=amount)

                return Response(SavingsJarSerializer(jar).data)
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
