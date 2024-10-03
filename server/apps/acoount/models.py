from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices
from PIL import Image
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from typing import Any


class DefaultModel(models.Model):
    """Абстрактный базовый класс модели, предоставляющий строковое представление."""
    class Meta:
        abstract = True

    def __str__(self) -> str:
        name = getattr(self, 'name', None)
        if name is not None:
            return str(name)
        return super().__str__()
    

def validator_avatar_size(file) -> None:
    """Валидатор размера файла для изображений."""
    limit = 5 * 1024 * 1024
    if file.size > limit:
        raise ValidationError('нюхай бебру')


class User(AbstractUser):

    class GENDERS(TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    gender = models.CharField(
        max_length=6,
        choices=GENDERS.choices,
        default=False,
        )
    avatar = models.ImageField(
        verbose_name='Avatar',
        upload_to='media/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validator_avatar_size,
        ]
    )
    is_verified = models.BooleanField(default=True)
    rating = models.IntegerField(default=0)


    def save(self, *args: Any, **kwargs: Any) -> None:
        """Метод для сохранения изображения."""
        super().save(*args, **kwargs)
        if self.avatar:
            try:
                image = Image.open(self.avatar.path)
                max_size = (228, 228)
                if image.height > 228 or image.width > 228:
                    image.thumbnail(max_size)
                    image.save(self.avatar.path)
            except Exception as e:
                raise ValidationError('пиздец!')



class Team(models.Model, DefaultModel):
    pass


class Tournament(models.Model):
    pass


class TournamentTeam(models.Model):
    pass