from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Idea,  IdeaComment, IdeaLikes, IdeaCommentLikes, IdeaSupporter


class IdeaAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_by', 'created_at', 'likes', )


class IdeaLikesAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea')


admin.site.register(Idea)
admin.site.register(IdeaLikes)
admin.site.register(IdeaComment)
admin.site.register(IdeaSupporter)
admin.site.register(IdeaCommentLikes)