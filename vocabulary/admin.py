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


admin.site.register(Word)

admin.site.register(UserWord)
