from django.urls import include, path
from rest_framework import routers
from .views import ArbiterViewSet, GenerateArbiters, get_arbiters_form

router = routers.DefaultRouter()
router.register("arbiter", ArbiterViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("generate-arbiters", GenerateArbiters.as_view(), name="generate-arbiters"),
    path("get-arbiters-form", get_arbiters_form, name="get-arbiters-form")
]