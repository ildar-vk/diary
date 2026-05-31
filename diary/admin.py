from django.contrib import admin
from .models import Entry, Category


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'entry_date', 'created_at')
    list_filter = ('category', 'entry_date', 'author')
    search_fields = ('title', 'content')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'keywords')
