from django.urls import path, include, re_path
from rest_framework import routers
from .views import UserViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')


urlpatterns = [
    path('', include(router.urls)),
    path('sign_up/', views.SocialSignUp.as_view(), name="sign_up"),
    path('login/', views.Login.as_view(), name="login"),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]