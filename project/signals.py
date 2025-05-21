from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task

@receiver(pre_save, sender=Task)
def notify_status_change(sender, instance, **kwargs):
    if instance.pk:
        old_status = Task.objects.get(pk=instance.pk).status # it is not updated.
        new_status = instance.status
        if old_status != new_status:
            print(" ----------------- Signal Triggeredd -----------------\n")
            print(f"Task '{instance.title}' status changed from {old_status} to {new_status}")

