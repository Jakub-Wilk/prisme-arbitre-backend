from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import ArbiterProfile, Language, Court, Location, Specialization


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["name", ]


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ["name", ]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["name", "lat", "long"]


class CourtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Court
        fields = ["location", "address"]


class SimpleArbiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbiterProfile
        fields = ["id", "first_name", "last_name", "photo", "verified", "email", "nationality", "description", "active"]


class ArbiterProfileSerializer(serializers.ModelSerializer):
    specializations = SpecializationSerializer(many=True, required=False)

    class Meta:
        model = ArbiterProfile
        fields = ["id", "first_name",
                  "last_name", "photo",
                  "verified", "email",
                  "nationality", "description",
                  "active", "languages",
                  "specializations", "experience",
                  "location", "court", "verification_document"]


class UserSerializer(ModelSerializer):
    arbiter_profile = SimpleArbiterProfileSerializer(read_only=True)

    class Meta:
        model = User
        depth = 1
        fields = ('id', "username", "date_joined", "arbiter_profile")


class CreateUserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        ArbiterProfile.objects.create(user=user)
        return user
