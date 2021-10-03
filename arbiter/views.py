import json, random, math

from django.contrib.auth.models import User

from .models import ArbiterProfile, Location, Court, Specialization, Language
from .jwt import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
from django.shortcuts import render
from django.db import transaction
from django.forms.models import model_to_dict
from django.contrib.staticfiles.storage import staticfiles_storage
from .serializers import ArbiterProfileSerializer, CreateUserProfileSerializer, LocationSerializer, \
    SpecializationSerializer, CourtSerializer, LanguageSerializer
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class ArbiterViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = ArbiterProfile.objects.all()
    serializer_class = ArbiterProfileSerializer

    # permission_classes = (IsAuthenticatedOrReadOnly,)

    # TODO: Permisje nie działają

    def list(self, request):
        # TODO: Zaimplementować customowy mechanizm wyszukiwania
        # queryset = ArbiterProfile.objects.all()
        queryset = get_relevant_arbiters(request.query_params)
        serializer = ArbiterProfileSerializer(queryset, many=True)
        return Response(serializer.data)
        # return Response(queryset)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserProfileSerializer


class GenerateArbiters(APIView):
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (TemplateHTMLRenderer,)

    def post(self, request):
        if request.data == {}:
            return Response(request.data, status=404, template_name="404.html")
        else:
            with open(staticfiles_storage.path("json/random_choices.json"), "r", encoding="utf-8") as file:
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


class LoadArbitersFromJSON(APIView):
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (TemplateHTMLRenderer,)

    @transaction.atomic
    def get(self, request):
        if ArbiterProfile.objects.filter(first_name="Janusz", last_name="Adamkowski").exists():
            return Response(request.query_params, status=403, template_name="403.html")
        with open(staticfiles_storage.path("json/data1-1.json"), "r", encoding="utf-8") as file:
            data1 = json.loads(file.read())
            for i in data1:
                i["court"] = "Sąd Arbitrażowy przy Krajowej Izbie Gospodarczej w Warszawie"
        with open(staticfiles_storage.path("json/data2-1.json"), "r", encoding="utf-8") as file:
            data2 = json.loads(file.read())
            for i in data2:
                i["court"] = "Sąd Arbitrażowy przy Konfederacji Lewiatan"
        with open(staticfiles_storage.path("json/locations.json"), "r", encoding="utf-8") as file:
            location_data = json.loads(file.read())
        data = data1 + data2
        for person in data:
            arbiter = ArbiterProfile()
            arbiter.save()
            for key, value in person.items():
                if key == "null" or value is None:
                    continue
                else:
                    if key == "languages":
                        for language in value:
                            existing_language = Language.objects.filter(name=language.lower())
                            if existing_language.exists():
                                language = existing_language.first()
                            else:
                                language = Language(name=language.lower())
                                language.save()
                            arbiter.languages.add(language)
                    elif key == "specializations":
                        for specialization in value:
                            existing_specialization = Specialization.objects.filter(name=specialization.lower())
                            if existing_specialization.exists():
                                specialization = existing_specialization.first()
                            else:
                                specialization = Specialization(name=specialization.lower())
                                specialization.save()
                            arbiter.specializations.add(specialization)
                    elif key == "degree":
                        arbiter.degree = True
                    elif key == "nationality":
                        arbiter.nationality = value.lower()
                    elif key == "location":
                        existing_location = Location.objects.filter(name=value.lower())
                        if existing_location.exists():
                            location = existing_location.first()
                        else:
                            location = Location(name=value.lower())
                            if value.lower() in location_data.keys():
                                location.lat, location.long = location_data[value.lower()]
                            location.save()
                        arbiter.location = location
                    elif key == "court":
                        existing_warszawa = Location.objects.filter(name="warszawa")
                        if existing_warszawa.exists():
                            location = existing_warszawa.first()
                        else:
                            location = Location(name="warszawa")
                            location.save()
                        court = Court(name=value.lower(), location=location)
                        court.save()
                        arbiter.court = court
                    elif key == "country":
                        arbiter.country = value.lower()
                    elif key == "experience":
                        arbiter.experience = value.lower()
                    elif key == "birth_year":
                        arbiter.birth_year = value.lower()
                    elif key == "photo":
                        arbiter.photo = value.lower()
                    elif key == "first_name":
                        arbiter.first_name = value.lower()
                        print("setting first name to", value, value.lower())
                    elif key == "last_name":
                        arbiter.last_name = value.lower()
                    else:
                        raise KeyError(key)
            arbiter.save()
            print("created object", arbiter)
        return Response(request.query_params, status=200, template_name="load-arbiters.html")


def calculate_distance_between(location1, location2):
    earth_radius = 6378.2064
    location1 = (location1.lat, location1.long)
    location2 = (location2.lat, location2.long)
    location1 = list(map(lambda n: n / (180 / math.pi), location1))
    location2 = list(map(lambda n: n / (180 / math.pi), location2))
    # d = earth_radius * acos((sin(lat1) * sin(lat2)) + cos(lat1) * cos(lat2) * cos(long2 – long1))
    return earth_radius * math.acos(
        (math.sin(location1[0]) * math.sin(location2[0])) + math.cos(location1[0]) * math.cos(location2[0]) * math.cos(
            location2[1] - location1[1]))


def get_relevant_arbiters(user_data):
    def determine_relevance(arbiter):
        relevance = 0
        if user_data.get("location", False) and arbiter.location:
            locations = (Location.objects.filter(name=user_data["location"].lower()).first(), arbiter.location)
            location_count = sum(map(lambda n: 1 if n.lat and n.long else 0, locations))
            if location_count == 2:
                distance = calculate_distance_between(locations[0], locations[1])
                relevance += 100 / (0.01 * distance + 1)
            elif user_data.get("court", False) and arbiter.court:
                locations = (Court.objects.filter(name=user_data["court"].lower()).first().location, arbiter.court.location)
                distance = calculate_distance_between(locations[0], locations[1])
                relevance += 100 / (0.01 * distance + 1)
        if user_data.get("languages", False) and arbiter.languages:
            languages = (
            map(lambda n: Language.objects.filter(name=n).first(), json.loads(user_data["languages"].lower())), list(arbiter.languages.all()))
            languages = list(map(lambda n: map(lambda m: m.name, n), languages))
            relevant_languages = set(list(languages[0])) & set(list(languages[1]))
            print(relevant_languages)
            relevance += len(relevant_languages) * 50
        if user_data.get("specializations", False) and arbiter.specializations:
            specializations = (
            map(lambda n: Specialization.objects.filter(name=n).first(), json.loads(user_data["specializations"].lower())),
            list(arbiter.specializations.all()))
            specializations = list(map(lambda n: map(lambda m: m.name, n), specializations))
            relevant_specializations = set(list(specializations[0])) & set(list(specializations[1]))
            relevance += len(relevant_specializations) * 50
        if user_data.get("court", False) and arbiter.court:
            court = Court.objects.filter(name=user_data["court"].lower()).first()
            if arbiter.court.name == court.name:
                relevance += 500
        if user_data.get("degree", False):
            if arbiter.degree:
                relevance += 200
        relevance += (100 * arbiter.votes) / (arbiter.votes + 100)
        return relevance

    arbiters = list(ArbiterProfile.objects.all())
    print(determine_relevance(arbiters[1]))
    return sorted(arbiters, key=determine_relevance, reverse=True)


class GetAllLocationsUnique(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Location.objects.all()

    serializer_class = LocationSerializer

    def list(self, request):
        queryset = Location.objects.all()
        serialized = LocationSerializer(queryset, many=True)
        return Response(serialized.data)


class GetAllLanguagesUnique(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Language.objects.all()

    serializer_class = LanguageSerializer

    def list(self, request):
        queryset = Language.objects.all()
        serialized = LanguageSerializer(queryset, many=True)
        return Response(serialized.data)


class GetAllSpecializationsUnique(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Specialization.objects.all()

    serializer_class = SpecializationSerializer

    def list(self, request):
        queryset = Specialization.objects.all()
        serialized = SpecializationSerializer(queryset, many=True)
        return Response(serialized.data)


class GetAllCourtsUnique(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Court.objects.all()

    serializer_class = CourtSerializer

    def list(self, request):
        queryset = Court.objects.all()
        serialized = CourtSerializer(queryset, many=True)
        return Response(serialized.data)
