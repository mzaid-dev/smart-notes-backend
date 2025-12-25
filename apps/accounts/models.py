from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    is_email_verified = models.BooleanField(default=False)

    otp = models.CharField(max_length=6,null=True,blank=True)
    otp_created_at = models.DateTimeField(null=True,blank=True)

    last_activity = models.DateTimeField(null=True,blank=True)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email



