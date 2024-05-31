from ninja import ModelSchema

from users.models import CustomUser


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
