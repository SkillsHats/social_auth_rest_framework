# import base64
# from django.conf import settings
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth import get_user_model
# from rest_framework import serializers

# User = get_user_model()


# class LoginSerializer(serializers.ModelSerializer):
#     user_client_id = serializers.SerializerMethodField('get_client_id')
#     user_client_secret = serializers.SerializerMethodField('get_client_secret')

#     class Meta:
#         model = User
#         fields = ('client_id', 'client_secret')

#     def get_client_id(self, obj, *args, **kwargs):
#         return obj.application_set.first().client_id

#     def get_client_secret(self, obj, *args, **kwargs):
#         return obj.application_set.first().client_secret


# class SignUpSerializer(LoginSerializer):
#     class Meta:
#         model = User
#         fields = ('name', 'email', 'password', 'user_client_id', 'user_client_secret',)
#         write_only_fields = ('password',)
#         