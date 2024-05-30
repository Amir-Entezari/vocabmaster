from pydantic import Field
from ninja import ModelSchema, Schema
from typing import Optional



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


