from django.db import models
from apps.core.models import TimestampedModel

# User Profile Model
class Profile(TimestampedModel):
    user = models.OneToOneField(
        'accounts.User', on_delete=models.CASCADE
    )
    bio             = models.TextField(null=True, blank=True)
    image           = models.URLField(blank=True)


    class Meta:
        db_table = 'profile'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.user.email

