from oauth2_provider.models import Application

def create_auth_client(sender, instance=None, created=False, **kwargs):
    if created:
        Application.objects.create(user=instance, client_type=Application.CLIENT_CONFIDENTIAL,
                                   authorization_grant_type=Application.GRANT_PASSWORD)