from django.urls import path

from .views import ProfileRetrieveAPIView

app_name = 'profiles'
urlpatterns = [
    path('profiles/<int:pk>/', ProfileRetrieveAPIView.as_view()),
]
