from pydantic import Field
from ninja import ModelSchema, Schema
from typing import Optional

from vocabulary.models import CustomUser


class WordInputSchema(Schema):
    word: str


class WordOutSchema(Schema):
    id: int
    word: str
    phonetic: Optional[str]
    audio_url: Optional[str]
    meaning: Optional[str]
    example_sentence: Optional[str]
    origin: Optional[str]
    part_of_speech: Optional[str]


class UserWordSchema(Schema):
    word: str
    user_note: Optional[str] = Field(None)


class UserWordOutSchema(Schema):
    id: int
    word: str
    added_at: str
    user_note: str


class LoginIn(ModelSchema):
    class Config:
        model = CustomUser
        model_fields = ["username", "password"]


class LogoutOut(ModelSchema):
    class Config:
        model = CustomUser
        model_fields = ["username", "email", "first_name", "last_name"]


class UserOut(ModelSchema):
    class Config:
        model = CustomUser
        model_fields = ["username", "email", "first_name", "last_name"]
