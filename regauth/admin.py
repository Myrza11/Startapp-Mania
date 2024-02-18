from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(CustomUsers)
admin.site.register(Works)
admin.site.register(Socials)