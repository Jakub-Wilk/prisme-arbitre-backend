from rest_framework_simplejwt.views import TokenObtainPairView
from .jwt import CustomTokenObtainPairSerializer
from .models import ArbiterProfile
from .serializers import ArbiterProfileSerializer
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ArbiterViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
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
