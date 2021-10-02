from .models import ArbiterProfile
from .serializers import ArbiterProfileSerializer
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response


class ArbiterViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = ArbiterProfile.objects.all()
    serializer_class = ArbiterProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request):
        # TODO: Zaimplementować customowy mechanizm wyszukiwania
        queryset = ArbiterProfile.objects.all()
        serializer = ArbiterProfileSerializer(queryset, many=True)
        return Response(serializer.data)
