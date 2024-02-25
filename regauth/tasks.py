from django.db import transaction


# import os
# import django
# import schedule
# import time
# from regauth.models import CustomUsers
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'startappmania.settings')
# django.setup()
#
#
# def delete_inactive_users():
#     CustomUsers.objects.filter(is_active=False).delete()
#     print("Inactive users deleted successfully.")
#
#
# schedule.every(5).minutes.do(delete_inactive_users)
#
#
# schedule.run_pending()