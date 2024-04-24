from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserInformation, Doctor, Patient

@receiver(post_save, sender=UserInformation)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_doctor:
            Doctor.objects.create(information=instance)
        else:
            Patient.objects.create(information=instance)
    else:
        if instance.is_doctor:
            Doctor.objects.update_or_create(information=instance)
        else:
            Patient.objects.update_or_create(information=instance)
