from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpRequest
from ninja import Router
from ninja.errors import HttpError

from .auth import user_auth, generate_token, blacklist_token
from .models import CustomUser as User
from .schemas import UserOut, LoginIn

router = Router()


@router.get("/", response=UserOut, auth=user_auth)
def fetch_user(request: HttpRequest):
    if request.auth.is_authenticated:
        return request.auth
    else:
        raise HttpError(401, "User not authenticated")


@router.post("/login")
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


@router.post("/logout", auth=user_auth)
def user_logout(request):
    logout(request)
    blacklist_token(request.headers.get("Authorization"))
