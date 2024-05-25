from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Word(models.Model):
    word = models.CharField(max_length=255)
    meaning = models.TextField()
    synonyms = models.ManyToManyField("self", blank=True)
    example_sentence = models.TextField(blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.word


class UserWord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    user_note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'word')

    def __str__(self):
        return f'{self.user.username} - {self.word.word}'