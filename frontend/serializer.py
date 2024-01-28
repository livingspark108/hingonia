from rest_framework import serializers

from apps.user.models import TransactionDetails


class TransactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetails
        fields = '__all__'


