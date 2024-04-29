

from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    
    mobile_number = models.CharField(max_length=15)  # Adjust max length as per your needs
    verification_sms_code = models.CharField(blank=True,max_length=6)  # Adjust max length as per your needs
    verification_email_code = models.CharField(blank=True,max_length=6)  # Adjust max length as per your needs
    
    is_sms_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    sms_time_for_valid = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username