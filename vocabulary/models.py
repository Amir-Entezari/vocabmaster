from django.db import models
from django.conf import settings


class Word(models.Model):
    word = models.CharField(max_length=255, unique=True)
    phonetic = models.CharField(max_length=255, blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    meaning = models.TextField()
    example_sentence = models.TextField(blank=True, null=True)
    origin = models.TextField(blank=True, null=True)
    part_of_speech = models.CharField(max_length=50, blank=True, null=True)
    synonyms = models.ManyToManyField('self', blank=True)
    extra_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.word


class UserWord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    user_note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'word')

    def __str__(self):
        return f'{self.user.username} - {self.word.word}'


