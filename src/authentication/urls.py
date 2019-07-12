from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('api.social.urls')),
    path('social/auth/', include('rest_framework_social_oauth2.urls')),
    path('api/v1/', include('api.accounts.urls', namespace='accounts')),
    path('api/v1/', include('api.profiles.urls', namespace='profiles')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)