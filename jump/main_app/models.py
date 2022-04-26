from django.contrib.auth import get_user_model
from django.db import models

from jump.common.validators import ValidateFileMaxSizeInMb

UserModel = get_user_model()


class Equip(models.Model):
    BOARD = 'Board'
    SAIL = 'Sail'
    MAST = 'Mast'
    BOOM = 'Boom'
    HARNESS = 'Harness'
    OTHER = 'Other'

    TYPES = [(x, x) for x in (BOARD, SAIL, MAST, BOOM, HARNESS, OTHER)]

    BRAND_MAX_LENGTH = 150

    brand = models.CharField(
        max_length=BRAND_MAX_LENGTH,
    )
    type = models.CharField(
        max_length=max(len(x) for (x, _) in TYPES),
        choices=TYPES,
    )
    date_of_manufacture = models.DateField(
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.brand}'

    class Meta:
        unique_together = ('user', 'brand') ### optional


class Photo(models.Model):
    IMAGE_MAX_SIZE_IN_MB = 5
    IMAGE_UPLOAD_TO_DIR = 'images/'
    photo = models.ImageField(
        upload_to=IMAGE_UPLOAD_TO_DIR,
        validators=(
            ValidateFileMaxSizeInMb(IMAGE_MAX_SIZE_IN_MB),
        ),
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    publication_date = models.DateTimeField(
        auto_now_add=True,
    )
    tagged_equip = models.ManyToManyField(
        Equip,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class Spot(models.Model):
    NAME_MAX_LENGTH = 50

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
    )
    picture = models.URLField()
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'
