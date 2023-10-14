from rest_framework import serializers
from django.contrib.auth.models import User
# from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PhoneNumberSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15)
    class Meta:
        model = User
        fields = ['phone_number']
    def validate_phone_number(self, value):
        if User.objects.filter(username=value,is_active=False).exists():
            raise serializers.ValidationError("This phone number is already registered and is not verified")
        if User.objects.filter(username=value,is_active=True).exists():
            raise serializers.ValidationError("This phone number is already registered and is verified")
        return value
