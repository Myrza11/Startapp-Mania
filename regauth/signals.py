
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(pre_save, sender=User)
def deactivate_inactive_users(sender, instance, **kwargs):
    if not instance.is_active:
        # Действия при установке is_active в False, например, удаление пользователя
        instance.delete()