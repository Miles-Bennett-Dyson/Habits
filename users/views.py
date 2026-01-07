from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import CreateUserSerializer, UserSerializer, SecureUserData


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)

        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer
        elif self.get_object() == self.request.user:
            return UserSerializer
        else:
            return SecureUserData
