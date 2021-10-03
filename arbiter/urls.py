from django.urls import include, path
from rest_framework import routers
from .views import ArbiterViewSet, GenerateArbiters, get_arbiters_form, UserViewSet, LoadArbitersFromJSON,\
    GetAllLocationsUnique, GetAllLanguagesUnique, GetAllSpecializationsUnique, GetAllCourtsUnique

router = routers.DefaultRouter()
router.register("arbiter", ArbiterViewSet)
router.register("location", GetAllLocationsUnique)
router.register("language", GetAllLanguagesUnique)
router.register("specialization", GetAllSpecializationsUnique)
router.register("court", GetAllCourtsUnique)
router.register("user", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("generate-arbiters", GenerateArbiters.as_view(), name="generate-arbiters"),
    path("get-arbiters-form", get_arbiters_form, name="get-arbiters-form"),
    path("load-arbiters", LoadArbitersFromJSON.as_view(), name="load-arbiters")
]