from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import serializers

from apps.core import utils as base_utils
from api.profiles.serializers import ProfileSerializer

User = get_user_model()


# Normal User or Student Serializer
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    profile      = ProfileSerializer(write_only=True)
    bio          = serializers.CharField(source='userprofile.bio', read_only=True)
    image        = serializers.CharField(source='userprofile.image', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'token', 'profile', 'name', 'bio', 'image',)

        read_only_fields = ('token',)

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        for (key, value) in profile_data.items():
            setattr(instance.userprofile, key, value)

        instance.userprofile.save()
        return instance



# User Registration Serializer
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'phone_number', 'age', 'gender', 'token']

    def create(self, validated_data):
        is_active=False
        # site=get_current_site(self.context['request'])
        site = settings.SITE_URL
        send_email=False
        return User.objects.create_user(is_active=is_active, site=site, send_email=send_email, **validated_data)


# User Login Serializer
class LoginSerializer(serializers.Serializer):
    email       = serializers.CharField(max_length=255)
    password    = serializers.CharField(max_length=128, write_only=True)
    token       = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        email       = data.get('email', None)
        password    = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )


        return {
            'id': user.pk,
            'name':user.name,
            'email': user.email,
            'token': user.token
        }

