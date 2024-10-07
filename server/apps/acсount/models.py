from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, QuerySet
from PIL import Image
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from typing import Any
from django.utils import timezone
    

def validator_avatar_weight(file: Any) -> None:
    """Валидатор размера файла для изображений."""
    limit = 5 * 1024 * 1024
    if file.size > limit:
        raise ValidationError('Превышен размер файла')


class User(AbstractUser):
    class GENDERS(TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    gender = models.CharField(
        max_length=6,
        choices=GENDERS.choices,
        default=None,
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


class Team(models.Model):
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
    
    def add_member(self, user: User, role: str = 'participant') -> None:
        """ 
        Добавляет пользователя в команду.
        Если пользователь уже в команде, выбрасывает исключение.
        """
        if not TeamMembership.objects.filter(team=self, user=user).exists():
            TeamMembership.objects.create(team=self, user=user, role=role)
            raise ValidationError(
                f'Пользователь {user.username} уже в команде'
            )

    def is_creator(self, user: User) -> bool:
        """Проверяет, является ли пользователь создателем команды."""
        try:
            membership = TeamMembership.objects.get(team=self, user=user)
            return membership.role == self.ROLECHOICES.CREATOR
        except TeamMembership.DoesNotExist:
            return False

    def remove_member(
            self,
            user_to_remove: User,
            current_user: User,
            current_user_role: str,
    ) -> None:
        """
        Удаляет пользователя из команды.
        Если пользователь не в команде, выдает исключение.
        Только для создателей команды.
        """
        if current_user_role != self.ROLECHOICES.CREATOR:
            raise ValidationError('Вы не являетесь создателем команды')
        if user_to_remove == current_user:
            raise ValidationError('Вы не можете удалить себя')
        try:
            member = TeamMembership.objects.get(
                team=self,
                user=user_to_remove
            )
            member.delete()
        except TeamMembership.DoesNotExist:
            raise ValidationError(
                f'Пользователь {user_to_remove.username} не в команде'
            )
    
    def set_status_active(
            self,
            current_user_role: str,
        ) -> None:
        """
        Устанавливает статус команды ACTIVE.
        Только для создателей команды.
        """
        if current_user_role != self.ROLECHOICES.CREATOR:
            raise ValidationError('Вы не являетесь создателем команды')
        if self.status == self.STATUS.ACTIVE:
            raise ValidationError('Статус уже установлен')
        self.status = self.STATUS.ACTIVE
        self.save()

    def set_status_disbanded(
            self,
            current_user_role: str,
        ) -> None:
        """
        Устанавливает статус команды DISBANED.
        Только для создателей команды.
        """
        if current_user_role != self.ROLECHOICES.CREATOR:
            raise ValidationError('Вы не являетесь создателем команды')
        if self.status == self.STATUS.DISBANED:
            raise ValidationError('Статус уже установлен')
        self.status = self.STATUS.DISBANED
        self.date_disbanded = timezone.now()
        self.save()

    def get_members(self) -> QuerySet[Any]:
        """Возвращает QuerySet участников команды."""
        return self.membership.select_related('user').all()
        


class TeamMembership(models.Model):
    class ROLECHOICES(TextChoices):
        CREATOR = 'creator', 'Creator'
        MEMBER = 'member', 'Member'

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