from django.urls import path, re_path
from django.conf.urls import url

# from rest_framework_jwt.views import verify_jwt_token

from .views import (
    LoginAPIView,
    RegistrationAPIView,
    UserRetrieveUpdateAPIView,

    UserEmailVerificationAPIView,
)

app_name = 'account'
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),

    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),

    # url(r'^api-token-verify/', verify_jwt_token),

    re_path(r'^verify/(?P<verification_key>.+)/$',
        UserEmailVerificationAPIView.as_view(),
        name='email_verify'),
]
