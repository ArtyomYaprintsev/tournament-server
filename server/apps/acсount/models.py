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
    
    

def validator_avatar_weight(file: Any) -> None:
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
        default=False, #?
        )
    avatar = models.ImageField(
        verbose_name='Avatar',
        upload_to='media/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validator_avatar_weight,
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
                raise ValidationError('Image size error')


class Team(models.Model, DefaultModel):
    class STATUS(TextChoices):
        ACTIVE = 'active', 'Active'
        AWAITING = 'awaiting', 'Awaiting'
        DISBANED = 'disbanded', 'Disbanded'

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название команды',
        )
    members = models.ManyToManyField(
        User,
        through='TeamMembership',
        related_name='teams',
        verbose_name='Участники команды',
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS.choices,
        default=STATUS.AWAITING,
        verbose_name='Статус команды',
    )
    description = models.CharField(
        max_length=250,
        default='',
        blank=True,
        verbose_name='Описание команды',
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания команды',
    )
    date_disbanded = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата роспуска команды',
    )
    class Meta:
        verbose_name='Команда'
        verbose_name_plural='Команды'

class TeamMembership(models.Model):
    class ROLECHOICES(TextChoices):
        CREATOR = 'creator', 'Creator'
        PARTICIPANT = 'participant', 'Participant'

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='membership',
        )
    user =  models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='membership',
    )
    role = models.CharField(
        max_length=10,
        choices=ROLECHOICES.choices,
        default=ROLECHOICES.CREATOR,
        verbose_name='Роль в команде',
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации в команде',
    )
    class Meta:
        unique_together = ('team', 'user')
        verbose_name='Участник команды'
        verbose_name_plural='Участники команды'


class Tournament(models.Model):
    pass


class TournamentTeam(models.Model):
    pass