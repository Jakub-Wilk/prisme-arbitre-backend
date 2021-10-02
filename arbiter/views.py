import json, random

from django.contrib.auth.models import User

from .jwt import CustomTokenObtainPairSerializer
from .models import ArbiterProfile, Location
from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
from .serializers import ArbiterProfileSerializer, CreateUserProfileSerializer
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView


class ArbiterViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = ArbiterProfile.objects.all()
    serializer_class = ArbiterProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # TODO: Permisje nie działają

    def list(self, request):
        # TODO: Zaimplementować customowy mechanizm wyszukiwania
        queryset = ArbiterProfile.objects.all()
        serializer = ArbiterProfileSerializer(queryset, many=True)
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserProfileSerializer



class GenerateArbiters(APIView):
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (TemplateHTMLRenderer,)

    def post(self, request):
        if request.data == {}:
            return Response(request.data, status=404, template_name="404.html")
        else:
            with open(staticfiles_storage.url("json/random_choices.json"), "r", encoding="utf-8") as file:
                random_choices = json.loads(file.read())
            sex = random.choice(("f", "m"))
            amount = int(request.data["amount"])
            for i in range(amount):
                arbiter = ArbiterProfile()
                arbiter.first_name = random.choice(random_choices[f"first_names_{sex}"])
                arbiter.last_name = random.choice(random_choices[f"last_names_{sex}"])
                location = Location(name=random.choice(random_choices["locations"]))
                location.save()
                arbiter.location = location
                arbiter.nationality = random.choice(random_choices["nationalities"])
                arbiter.save()
            return Response({"stage": "confirm", "arbiters": ArbiterProfile.objects.all().values(), "amount": amount},
                            template_name="generate-arbiters-intermediate.html")


def get_arbiters_form(request):
    return render(request, "generate-arbiters-intermediate.html",
                  {"stage": "entry", "arbiters": ArbiterProfile.objects.all().values()})
