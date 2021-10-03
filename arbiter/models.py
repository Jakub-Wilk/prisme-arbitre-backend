from django.db import models
from django.contrib.auth.models import User


# User
# first_name
# last_name
# email
# date_joined
# username
# is_staff

class ArbiterProfile(models.Model):
    photo = models.ImageField(blank=True, null=True, upload_to="photos/")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="arbiter_profile", null=True, blank=True)
    verified = models.BooleanField(default=False)
    degree = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)
    location = models.ForeignKey("Location", on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(blank=True, null=True, max_length=255)
    nationality = models.CharField(blank=True, null=True, max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    court = models.ForeignKey("Court", related_name="arbiters", on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    description = models.CharField(blank=True, null=True, max_length=255)
    active = models.BooleanField(default=False, blank=True, null=True)
    birth_year = models.IntegerField(blank=True, null=True)
    experience = models.CharField(blank=True, null=True, max_length=65535)
    verification_document = models.FileField(blank=True, null=True, upload_to="documents/")

    def __str__(self):
        return f"{self.pk} - Arbiter Profile"


class Location(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)


class Language(models.Model):
    arbiter = models.ManyToManyField(ArbiterProfile, related_name="languages", blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    arbiter = models.ManyToManyField(ArbiterProfile, related_name="specializations", blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Court(models.Model):
    name = models.CharField(max_length=255)
    location = models.ForeignKey("Location", on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name
