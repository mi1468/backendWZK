from django.contrib import admin

from core.models.Patient import Patient
from core.models.role import Role
# from .model import user
from core.models.AssignedRule import AssignedRule
 

admin.site.register(Role)
admin.site.register(AssignedRule)
admin.site.register(Patient)
