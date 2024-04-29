from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    birthday = models.DateField(blank=True, null=True)
    patient_id = models.CharField(max_length=100, blank=True, null=True)

 

    pass

    # permissions = [('can_view_content', 'Can view content'), ('can_edit_content', 'Can edit content')]
    # groups = [('can_view_content', 'Can view content'), ('can_edit_content', 'Can edit content')]

# User._meta.get_field('user_permissions').remote_field.related_name = 'user_permissions_user'

    