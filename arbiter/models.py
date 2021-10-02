from django.db import models
from django.contrib.auth.models import User


class ArbiterProfile(models.Model):
    photo = models.ImageField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="arbiter_profile")
    verified = models.BooleanField(default=False)
    court = models.ForeignKey("Court", related_name="arbiters", on_delete=models.CASCADE)
    email = models.EmailField(blank=False, null=False)
    nationality = models.CharField(blank=True, null=True, max_length=255)
    description = models.CharField(blank=True, null=True, max_length=255)
    active = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"{self.pk} - Arbiter Profile"


class Language(models.Model):
    arbiter = models.ForeignKey(ArbiterProfile, related_name="languages", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    arbiter = models.ManyToManyField(ArbiterProfile, related_name="specializations", blank=True, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Experience(models.Model):
    arbiter = models.ForeignKey(ArbiterProfile, related_name="experience", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    period = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Court(models.Model):
    name = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name
