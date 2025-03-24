from rest_framework import serializers
from django.conf import settings
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']
        write_only_fileds = ['password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = Profile
