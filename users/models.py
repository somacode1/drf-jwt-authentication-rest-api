from datetime import datetime, timedelta
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import jwt 

from users.managers import CustomUserManager

SECRET_KEY = getattr(settings, 'SECRET_KEY', None)

class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser,Timestamp):
    id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, primary_key=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    # avatar = CloudinaryField('avatar', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)
    
    objects = CustomUserManager()
    
    
    # def __str__(self):
    #     return self.display_name
    
    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)
        exp_timestamp = int(dt.timestamp())
        
        token = jwt.encode({'id': str(self.pk),'exp': exp_timestamp}, SECRET_KEY, algorithm='HS256')
        
        return token

