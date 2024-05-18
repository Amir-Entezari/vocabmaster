from django.contrib import admin

from vocabulary.models import Word, UserWord

admin.site.register(Word)

admin.site.register(UserWord)
