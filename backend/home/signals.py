from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from home.models import StudentProfile


@receiver(post_save, sender=User)
def create_superuser_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        StudentProfile.objects.create(user=instance)
