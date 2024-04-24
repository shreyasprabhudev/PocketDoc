from django.contrib import admin
from .models import UserInformation, Doctor, Patient

admin.site.register(UserInformation)
admin.site.register(Doctor)
admin.site.register(Patient)