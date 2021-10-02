from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from arbiter.serializers import UserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        token['user'] = user_data
        return token
