from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from vocabulary.models import Word, UserWord, CustomUser


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )
    list_display = [
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_superuser",
    ]


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

