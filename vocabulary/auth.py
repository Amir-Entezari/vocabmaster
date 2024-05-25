from datetime import datetime
from datetime import timedelta
from .models import CustomUser, BlackToken
from .utils import (
    encrypt_string,
    decrypt_string,
    datetime_to_string,
    string_to_datetime,
    generate_random_string,
)


def generate_token(user: CustomUser) -> str:
    return encrypt_string(
        f"{user.id}.{datetime_to_string(datetime.now() + timedelta(days=365))}.{generate_random_string(4)}"
    )


def blacklist_token(token: str) -> None:
    BlackToken.objects.get_or_create(token=token)


def check_token(token_cipher: str) -> CustomUser | None:
    if not token_cipher:
        return False
    if BlackToken.objects.filter(token=token_cipher).count():
        return False
    try:
        token = decrypt_string(token_cipher)
    # TODO: add exceptions to except as this is not a good practice
    except:
        return False
    user_id_str, expiry_datetime, _ = token.split(".")
    if datetime.now() > string_to_datetime(expiry_datetime):
        return False
    try:
        return CustomUser.objects.get(id=int(user_id_str))
    except CustomUser.DoesNotExist:
        return False


def user_auth(request):
    user = check_token(request.headers.get("Authorization"))
    if user:
        # this sets request.auth to user
        return user
    else:
        return False