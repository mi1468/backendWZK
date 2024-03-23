# models.py
from django.contrib.auth.models import User
from .role import Role
from django.db import models

class AssignedRule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    # Add any other fields you need
