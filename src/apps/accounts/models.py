import jwt

import re
import hashlib
import datetime

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from apps.core import utils as base_utils
from apps.core.models import TimestampedModel, Verification


SHA1_RE = re.compile('^[a-f0-9]{40}$')
token_generator = default_token_generator


#  Custom User Manager
class UserManager(BaseUserManager):
    # Create User
    def _create_user(self, email, password, is_active=False, site=None, send_email=True, **extra_fields):

        if email is None:
            raise TypeError('User must have an email address.')

        email = self.normalize_email(email)

        hash_input = (get_random_string(5) + email).encode('utf-8')
        verification_key = hashlib.sha1(hash_input).hexdigest() # Verification Key for EMail Verification

        user = self.model(email=email, verification_key=verification_key, **extra_fields)

        user.set_password(password)
        user.is_active = is_active

        user.save(using=self._db)

        return user

    # Create Normal User
    def create_user(self, email=None, password=None, is_active=False, site=None, send_email=True, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self._create_user(email, password, is_active, site, send_email, **extra_fields)
        
        if send_email:
            user.send_activation_email(site)
        
        return user

    # Create Super User
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, is_active=True, site=None, send_email=False, **extra_fields)

    # Activate User
    def activate_user(self, verification_key):

        if SHA1_RE.search(verification_key.lower()):
            try:
                user = self.get(verification_key=verification_key)
            except ObjectDoesNotExist:
                return None
            if not user.verification_key_expired():
                user.is_active = True
                user.verification_key = User.ACTIVATED
                user.has_email_verified = True
                user.save()

                return user
        return None

    # Check Token Expired or Not
    def expired(self):

        now = timezone.now() if settings.USE_TZ else datetime.datetime.now()

        return self.exclude(
            models.Q(user__is_active=True) |
            models.Q(verification_key=User.ACTIVATED)
            ).filter(
                user__date_joined__lt=now - datetime.timedelta(
                    getattr(settings, 'VERIFICATION_KEY_EXPIRY_DAYS', 4)
                )
            )

    @transaction.atomic
    def delete_expired_users(self):
        for user in self.expired():
            user = profile.user
            profile.delete()
            user.delete()


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin, TimestampedModel, Verification):

    ACTIVATED = "ALREADY ACTIVATED"

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    name      		= models.CharField(max_length=255)
    email           = models.EmailField(db_index=True, unique=True)
    phone_number  	= models.CharField(max_length=16, blank=True)
    age 			= models.IntegerField(null=True, blank=True)
    gender 			= models.CharField(max_length=12, choices=GENDER_CHOICES, null=True, blank=True)

    verification_key = models.CharField(
        max_length=40
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )


    USERNAME_FIELD  = 'email'
    # REQUIRED_FIELDS = ['email']

    objects = UserManager()

    # META CLASS
    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    # Generate Verfication Key
    def verification_key_expired(self):

        expiration_date = timedelta(
            days=getattr(settings, 'VERIFICATION_KEY_EXPIRY_DAYS', 4)
        )

        return self.verification_key == self.ACTIVATED or \
               (self.created_at + expiration_date <= timezone.now())

    # Send Email Verification Mail
    def send_activation_email(self, site):

        context = {
            'verification_key': self.verification_key,
            'expiration_days': getattr(settings, 'VERIFICATION_KEY_EXPIRY_DAYS', 4),
            'user': self,
            'site': site,
            'site_name': getattr(settings, 'SITE_NAME', None)
        }

        subject = render_to_string(
            'registration/activation_email_subject.txt', context
        )

        subject = ''.join(subject.splitlines())

        message = render_to_string(
            'registration/activation_email_content.txt', context
        )

        msg = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(message, "text/html")
        msg.send()


    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def _generate_jwt_token(self):

        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
