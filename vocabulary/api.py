from datetime import datetime
from sqlite3 import IntegrityError
from typing import List

from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpRequest
from ninja import NinjaAPI, Router
from ninja.errors import HttpError
from ninja.orm import create_schema
# from django.contrib.auth.models import User

from .auth import user_auth, generate_token, blacklist_token
from .models import Word, UserWord
from .models import CustomUser as User
from .schemas import WordInputSchema, WordOutSchema, UserWordOutSchema, UserOut, LoginIn
from .utils import fetch_word_data

api = NinjaAPI()

router = Router()


@router.get("/user", response=UserOut, auth=user_auth)
def fetch_user(request: HttpRequest):
    if request.auth.is_authenticated:
        return request.auth
    else:
        raise HttpError(401, "User not authenticated")


@router.post("user/login")
def user_login(request: HttpRequest, payload: LoginIn) -> HttpResponse:
    try:
        user = User.objects.get(username=payload.username)
        if user.check_password(payload.password):
            login(request, user)
            return HttpResponse(generate_token(user), status=200)
        else:
            return HttpResponse("Wrong username or password", status=401)
    except User.DoesNotExist:
        return HttpResponse("Wrong username or password", status=401)


@router.post("user/logout", auth=user_auth)
def user_logout(request):
    logout(request)
    blacklist_token(request.headers.get("Authorization"))

