from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import ArbiterProfile


class ArbiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbiterProfile
        fields = ["first_name", "last_name", "photo", "verified", "email", "nationality", "description", "active"]


class UserSerializer(ModelSerializer):
    arbiter_profile = ArbiterProfileSerializer(read_only=True)

    class Meta:
        model = User
        depth = 1
        fields = ('id', "username", "date_joined", "arbiter_profile")
