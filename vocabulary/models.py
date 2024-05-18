from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=255)
    meaning = models.TextField()
    synonyms = models.ManyToManyField("self", blank=True)
    example_sentence = models.TextField(blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.word
