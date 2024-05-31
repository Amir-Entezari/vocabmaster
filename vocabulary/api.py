from datetime import datetime
from typing import List

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError
from ninja.orm import create_schema

from users.auth import user_auth
from .models import Word, UserWord
from .schemas import WordInputSchema, WordOutSchema
from .utils import fetch_word_data

# from django.contrib.auth.models import User


router = Router()


# TODO: write schema for UserWordSchema
@router.post("users/words", response=WordOutSchema, auth=user_auth)
def user_create_word(request, payload: WordInputSchema):
    try:
        word_instance = Word.objects.get(word=payload.word)
        user_word = UserWord.objects.get(user=request.user, word=word_instance)
        raise HttpError(400, "Word already exists.")
    except Word.DoesNotExist:
        word = fetch_word_data(payload.word)
        word_instance = Word.objects.create(**word)
        user_word = UserWord.objects.create(user=request.user, word=word_instance)
    except UserWord.DoesNotExist:
        user_word = UserWord.objects.create(user=request.user, word=word_instance).select_related('word')
    return user_word.word


@router.get("users/words",
            response=List[create_schema(
                Word,
                optional_fields="__all__",
                custom_fields=[('user_note', str, None), ("added_at", datetime, None)],
            )],
            auth=user_auth)
def get_list_user_words(request):
    # user_words = UserWord.objects.filter(user=request.user).select_related('word')
    user_words = UserWord.objects.select_related('word').filter(user=request.auth).prefetch_related('word__synonyms')

    return [
        {
            "word": user_word.word.word,
            "phonetic": user_word.word.phonetic,
            "audio_url": user_word.word.audio_url,
            "meaning": user_word.word.meaning,
            "example_sentence": user_word.word.example_sentence,
            "origin": user_word.word.origin,
            "part_of_speech": user_word.word.part_of_speech,
            "synonym": [synonym.word for synonym in user_word.word.synonyms.all()],
            "extra_info": user_word.word.extra_info,
            "added_at": user_word.added_at,
            "user_note": str(user_word.user_note)
        }
        for user_word in user_words
    ]


@router.put(
    path="users/word/{str:word}",
    auth=user_auth,
    response=create_schema(
        UserWord,
        fields=[
            'user',
            'word',
            'added_at',
            'user_note',
        ],
        optional_fields="__all__",
    ),
)
def update_user_word(
        request: HttpRequest,
        payload: create_schema(
            UserWord,
            fields=[
                'user_note'
            ],
            optional_fields="__all__",
        ),
        word,
):
    try:
        user_word = UserWord.objects.get(user=request.user, word__word=word)
        for field, value in payload.dict().items():
            setattr(user_word, field, value)
        user_word.save(update_fields=payload.dict(exclude_none=True).keys())
        return user_word
    except UserWord.DoesNotExist:
        raise HttpError(404, "UserWord does not exist")


@router.delete("users/words/{str:word}", auth=user_auth)
def delete_user_word(request: HttpRequest, word):
    try:
        user = UserWord.objects.get(word__word=word, user=request.user)
        user.delete()
    except UserWord.DoesNotExist:
        raise HttpError(404, "User does not have this word.")


@router.get("words/{str:word}", response=WordOutSchema)
def get_word(request, word):
    try:
        word_instance = Word.objects.get(word=word)
        return word_instance
    except Word.DoesNotExist:
        raise HttpError(404, "Word does not exist.")
