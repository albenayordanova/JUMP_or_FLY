from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models

from jump.auth_app.managers import JumpUserManager
from jump.common.validators import only_letters_validator


class JumpUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LENGTH = 40
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    USERNAME_FIELD = 'username'

    objects = JumpUserManager()


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 25
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 25

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            only_letters_validator,
        )
    )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            only_letters_validator,
        )
    )
    picture = models.URLField()
    phone = models.IntegerField()
    email = models.EmailField(
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        JumpUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


