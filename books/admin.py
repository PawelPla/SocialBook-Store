from django.contrib import admin
from django.contrib.admin import ModelAdmin

from books.models import Book, Review


class ReviewInLine(admin.TabularInline):
    model = Review


class BookAdmin(ModelAdmin):
    inlines = [ReviewInLine, ]
    list_display = ('title', 'author', 'price',)


admin.site.register(Book, BookAdmin)
