from django.conf import settings
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    phone_no = PhoneNumberField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.TextField(null=True, blank=True)
    
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def __str__(self):
        full_name = self.get_full_name().strip()
        if not full_name:
            return self.user.username
        return full_name
