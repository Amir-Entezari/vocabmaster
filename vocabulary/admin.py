from django.contrib import admin

from vocabulary.models import Word, UserWord


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    # autocomplete_fields = ['word']
    list_display = ['id', 'word', 'meaning']
    search_fields = ['word']


@admin.register(UserWord)
class UserWordAdmin(admin.ModelAdmin):
    autocomplete_fields = ['word']
    list_display = ['id', 'word', 'added_at', 'user_note']
    search_fields = ['word']
