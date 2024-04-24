from django.conf import settings
from django.db import models

class UserInformation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userinformation')
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Doctor(models.Model):
    information = models.OneToOneField(UserInformation, on_delete=models.CASCADE, primary_key=True)
    specialty = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.information.first_name} {self.information.last_name} - {self.specialty}"

class Patient(models.Model):
    information = models.OneToOneField(UserInformation, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(null=True, blank=True) 

