import base64
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

__author__ = 'shyam'

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    client_id = serializers.SerializerMethodField('get_client_id')
    client_secret = serializers.SerializerMethodField('get_client_secret')

    class Meta:
        model = User
        fields = ('client_id', 'client_secret')

    def get_client_id(self, obj, *args, **kwargs):
        return obj.application_set.first().client_id

    def get_client_secret(self, obj, *args, **kwargs):
        return obj.application_set.first().client_secret


class SignUpSerializer(LoginSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'client_id', 'client_secret',)
        write_only_fields = ('password',)
        


class BaseModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(BaseModelSerializer, self).__init__(*args, **kwargs)
        self.fields['content_type'] = serializers.SerializerMethodField('get_content_type')

    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj).pk


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        custom_user_serializer = get_class(settings.USER_SERIALIZER)
        self.fields = custom_user_serializer().fields