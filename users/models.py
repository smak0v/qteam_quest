from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from korobka_games.settings import ROOT_URL
from users.managers import UserManager

GENDERS = [
    ('NOT_SET', 'Не установлена'),
    ('MALE', 'Мужчина'),
    ('FEMALE', 'Женщина'),
]

POSITIONS = [
    ('NOT_SET', 'Не установлена'),
    ('GOALIE', 'Вратарь'),
    ('DEFENDER', 'Защитник'),
    ('MIDFIELDER', 'Полузащитник'),
    ('FORWARD', 'Нападающий'),
]


class User(AbstractBaseUser):
    """Class thar represents user"""

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_profile_image(self):
        if not self.profile_image:
            return ROOT_URL + '/static/img/no_user.png'
        return ROOT_URL + self.profile_image.url

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=255,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255,
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=255,
        unique=True,
    )
    location = models.CharField(
        verbose_name='Локация',
        max_length=255,
        default='',
    )
    gender = models.CharField(
        verbose_name='Пол',
        max_length=255,
        choices=GENDERS,
        default='NOT_SET',
    )
    nationality = models.CharField(
        verbose_name='Национальность',
        max_length=255,
        default='',
    )
    favourite_position = models.CharField(
        verbose_name='Любимая позиция',
        max_length=255,
        choices=POSITIONS,
        default='NOT_SET',
    )
    active = models.BooleanField(
        verbose_name='Активный',
        default=True,
    )
    staff = models.BooleanField(
        verbose_name='Персонал',
        default=False,
    )
    admin = models.BooleanField(
        verbose_name='Администратор',
        default=False,
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=15,
        null=True,
        blank=True,
        default='',
    )
    phone_activation_code = models.IntegerField(
        verbose_name='Последний код активации номера телефона',
        default=None,
        null=True,
        blank=True,
    )
    is_active_phone = models.BooleanField(
        verbose_name='Номер телефона подтвержден',
        default=False,
    )
    reliability = models.DecimalField(
        verbose_name='Надежность',
        decimal_places=2,
        max_digits=5,
        blank=True,
        default=100,
    )
    profile_image = models.ImageField(
        verbose_name='Фото профиля',
        upload_to='images/profile_images',
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'email',
    ]

    objects = UserManager()

    def __str__(self):
        return '{}'.format(self.username)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return '{}'.format(self.username)

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class UserAuthToken(models.Model):
    """Class that represents user auth token model"""

    class Meta:
        verbose_name = 'Токен авторизации'
        verbose_name_plural = 'Токены авторизации'

    token = models.CharField(
        verbose_name='Токен',
        max_length=255,
    )

    def __str__(self):
        return self.token


class UserChangePhone(models.Model):
    """Class that represents user change phone model"""

    class Meta:
        verbose_name = 'Изменение номера телефона'
        verbose_name_plural = 'Изминение номеров телефонов'

    phone = models.CharField(
        verbose_name='Телефон',
        max_length=15,
    )

    def __str__(self):
        return self.phone


class UserChangePhoneConfirm(models.Model):
    """Class that represents user change phone confirm model"""

    class Meta:
        verbose_name = 'Подтверждение изменения номера телефона'
        verbose_name_plural = 'Подтверждения изминений номеров телефонов'

    sms_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=5,
    )

    def __str__(self):
        return self.sms_code


class UserSubscription(models.Model):
    """Class that represent user subscription model"""

    class Meta:
        verbose_name = 'Подписка на пользователя'
        verbose_name_plural = 'Подписки на пользователей'

    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='users.User',
        on_delete=models.CASCADE,
    )
    subscriber = models.ForeignKey(
        verbose_name='Подписчик',
        to='users.User',
        on_delete=models.CASCADE,
        related_name='user_subscriptions',
    )

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.subscriber.username)
