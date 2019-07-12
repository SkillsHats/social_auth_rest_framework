import base64

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import APIException
# # from social.apps.django_app.utils import load_strategy
# # from social.apps.django_app.utils import load_backend

from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.exceptions import AuthAlreadyAssociated

from api.accounts.serializers import UserSerializer

from .serializers import SignUpSerializer,  LoginSerializer
from .permissions import IsAuthenticatedOrCreate, IsOwnerOrReadOnly


User = get_user_model()


class SocialSignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)


class Login(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    authentication_classes = (BasicAuthentication,)

    def get_queryset(self):
        return [self.request.user]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    @list_route(methods=["get"])
    def me(self, request):
        if request.user.is_authenticated:
            serializer = self.get_serializer(instance=request.user)
            return Response(serializer.data)
        else:
            return Response({"errors": "User is not authenticated"}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['patch'])
    def password(self, request, pk=None):
        user = self.get_object()
        if not user.check_password(base64.decodestring(request.DATA['old_password'])):
            raise APIException("Old password does not match")

        serializer = PasswordSerializer(data=request.DATA)
        if serializer.is_valid():
            user.set_password(base64.decodestring(serializer.data['password']))
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)