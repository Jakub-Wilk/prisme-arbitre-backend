from rest_framework import serializers
from .models import ArbiterProfile

class ArbiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbiterProfile
        fields = ["photo", "verified", "email", "nationality", "description", "active"]