from django.db import transaction
from .models import CustomUsers

# Асинхронная функция для удаления неактивированных пользователей
@transaction.atomic
async def cleanup_inactive_users():
    users_to_delete = CustomUsers.objects.filter(is_active=False)
    users_to_delete.delete()