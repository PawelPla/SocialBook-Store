from django.contrib import admin
from django.contrib.admin import ModelAdmin

from blog.models import Post, Comment


class ReviewInLine(admin.TabularInline):
    model = Comment


class PostAdmin(ModelAdmin):
    inlines = [ReviewInLine, ]
    list_display = ('title', 'author', 'content', 'date_posted',)


admin.site.register(Post, PostAdmin)
