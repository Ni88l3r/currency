from account.models import User

from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_active')
