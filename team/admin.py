from django.contrib import admin
from .models import Chat, Message, Team, Invitation
# Register your models here.
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Team)
admin.site.register(Invitation)