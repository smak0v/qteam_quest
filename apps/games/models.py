from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from apps.teams.models import UserInTeam, ReservedPlaceInTeam

PAYMENT_METHODS = [
    ('ONLINE', 'Онлайн оплата'),
]

CURRENCIES = [
    ('RUB', 'Рубли'),
]

GAME_STATUSES = [
    ('PUBLIC', 'Публичная игра'),
    ('PRIVATE', 'Частная игра'),
]

NUMBER_OF_PLAYERS_PER_TEAM = [
    ('5', '5 со стороны'),
    ('6', '6 со стороны'),
    ('7', '7 со стороны'),
    ('8', '8 со стороны'),
    ('9', '9 со стороны'),
    ('10', '10 со стороны'),
    ('11', '11 со стороны'),
]

GAME_LEVELS = [
    ('1', 'Начальный'),
    ('2', 'Любительский'),
    ('3', 'Проффесиональный'),
]


class Game(models.Model):
    """Class that represents game"""

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    title = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=900,
        default='',
        blank=True,
    )
    cover_image = models.ImageField(
        verbose_name='Обложка',
        upload_to='images/game_covers',
        null=True,
        default=None,
        blank=True,
    )
    photo = models.ImageField(
        verbose_name='Фото игры',
        upload_to='images/game_photos',
        null=True,
        default=None,
        blank=True,
    )
    timespan = models.DateTimeField(
        verbose_name='Дата и время',
    )
    duration = models.PositiveIntegerField(
        verbose_name='Длительность (в минутах)',
    )
    venue = models.ForeignKey(
        verbose_name='Площадка',
        to='venues.Venue',
        on_delete=models.CASCADE,
    )
    payment_method = models.CharField(
        verbose_name='Способ оплаты',
        max_length=255,
        choices=PAYMENT_METHODS,
        default='ONLINE',
    )
    level = models.CharField(
        verbose_name='Уровень игры',
        max_length=255,
        choices=GAME_LEVELS,
        default='1',
    )
    price = models.DecimalField(
        verbose_name='Цена',
        decimal_places=2,
        max_digits=15,
        default=0,
    )
    currency = models.CharField(
        verbose_name='Валюта',
        max_length=255,
        choices=CURRENCIES,
        default='RUB',
    )
    refund_money_if_game_is_cancelled = models.BooleanField(
        verbose_name='Возврат денег в случае отмены',
        default=False,
    )
    refundable_days = models.IntegerField(
        verbose_name='Возврат денег в случае отмены и предоставления уведомления за n дней',
        default=0,
    )
    game_status = models.CharField(
        verbose_name='Статус',
        max_length=255,
        choices=GAME_STATUSES,
        default='PUBLIC',
    )
    a_side_players_count = models.CharField(
        verbose_name='Количество игроков с одной команды',
        max_length=255,
        choices=NUMBER_OF_PLAYERS_PER_TEAM,
        default='5',
    )
    registration_available = models.BooleanField(
        verbose_name='Открыта для регистрации',
        default=True,
    )
    cancel = models.BooleanField(
        verbose_name='Отменить',
        default=False,
    )

    def check_registration_availability(self):
        timespan = timezone.now()
        if timespan.date() != self.timespan.date():
            return
        if self.timespan - timespan <= timezone.timedelta(hours=1):
            self.registration_available = False
            self.save()
            if not self.check_game_filling():
                self.cancel_game()
            return
        return

    def check_game_filling(self):
        total_players_count = int(self.a_side_players_count) * 2
        players_count = 0
        reserved_places_count = 0
        try:
            players_count = UserInTeam.objects.filter(game=self).count()
        except UserInTeam.DoesNotExist:
            players_count = 0
        try:
            reserved_places_count = ReservedPlaceInTeam.objects.filter(game=self).count()
        except ReservedPlaceInTeam.DoesNotExist:
            reserved_places_count = 0
        if players_count + reserved_places_count < total_players_count:
            return False
        elif players_count + reserved_places_count > total_players_count:
            return False
        return True

    def cancel_game(self):
        self.cancel = True
        self.save()

    def __str__(self):
        return '{}'.format(self.title)


class GameComment(models.Model):
    """Class that represents a game comment"""

    class Meta:
        verbose_name = 'Комментарий к игре'
        verbose_name_plural = 'Комментарии к игре'

    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='users.User',
        on_delete=models.CASCADE,
    )
    game = models.ForeignKey(
        verbose_name='Игра',
        to='games.Game',
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(
        verbose_name='Дата и время',
        auto_now_add=True,
    )
    text = models.CharField(
        verbose_name='Комментарий',
        max_length=900,
    )

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.game.title)


class GamePlayerEvaluation(models.Model):
    """Class that represents a player evaluation for a game"""

    class Meta:
        verbose_name = 'Оценка участника'
        verbose_name_plural = 'Оценки участников'

    game = models.ForeignKey(
        verbose_name='Игра',
        to='games.Game',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    appraiser = models.ForeignKey(
        verbose_name='Оценщик',
        to='users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ranked_user = models.ForeignKey(
        verbose_name='Оцениваемый',
        to='users.User',
        on_delete=models.CASCADE,
        related_name='ranked_user',
    )
    game_level = models.PositiveIntegerField(
        verbose_name='Уровень игры',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    enjoyed_playing = models.PositiveIntegerField(
        verbose_name='Понравилось играть',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
