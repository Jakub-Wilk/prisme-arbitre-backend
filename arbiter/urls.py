from django.urls import include, path
from rest_framework import routers
from .views import ArbiterViewSet

router = routers.DefaultRouter()
router.register("arbiter", ArbiterViewSet)

urlpatterns = [
    path("", include(router.urls))
]