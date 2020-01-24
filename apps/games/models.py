from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from apps.teams.models import UserInTeam

PAYMENT_METHODS = [
    ('ONLINE', 'Онлайн оплата'),
]

PAYMENT_STATUSES = [
    ('PENDING', 'Pending'),
    ('WAITING_FOR_CAPTURE', 'Waiting for capture'),
    ('SUCCEEDED', 'Succeeded'),
    ('CANCELED', 'Canceled'),
]

REFUND_STATUSES = [
    ('SUCCEEDED', 'Succeeded'),
    ('CANCELED', 'Canceled'),
]

CURRENCIES = [
    ('RUB', 'Рубли'),
]

GAME_LEVELS = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]


class Game(models.Model):
    """Class that represents game"""

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = [
            'timespan',
        ]

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
    genre = models.CharField(
        verbose_name='Жанр',
        max_length=255,
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
    quest = models.ForeignKey(
        verbose_name='Квест',
        to='quests.Quest',
        on_delete=models.CASCADE,
    )
    payment_method = models.CharField(
        verbose_name='Способ оплаты',
        max_length=255,
        choices=PAYMENT_METHODS,
        default='ONLINE',
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
    level = models.CharField(
        verbose_name='Уровень игры',
        max_length=255,
        choices=GAME_LEVELS,
        default='1',
    )
    refund_money_if_game_is_cancelled = models.BooleanField(
        verbose_name='Возврат денег в случае отмены',
        default=False,
    )
    refundable_days = models.IntegerField(
        verbose_name='Возврат денег в случае отмены и предоставления уведомления за n дней',
        default=0,
    )
    min_players_count = models.PositiveIntegerField(
        verbose_name='Минимальное количество игроков в команде',
    )
    max_players_count = models.PositiveIntegerField(
        verbose_name='Максимальное количество игроков в команде',
    )
    players_count = models.PositiveIntegerField(
        verbose_name='Количество игроков',
        default=0,
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
        if self.timespan - timespan <= timezone.timedelta(hours=1):
            self.registration_available = False
            self.save()
            if not self.check_game_filling():
                self.cancel_game()
        if self.timespan.date().day < timespan.date().day:
            self.registration_available = False
        return

    def check_game_filling(self):
        total_players_count = int(self.max_players_count)
        try:
            players_count = UserInTeam.objects.filter(game=self).count()
        except UserInTeam.DoesNotExist:
            players_count = 0
        if players_count < total_players_count:
            return False
        elif players_count > total_players_count:
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
        ordering = [
            '-timestamp',
        ]

    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='users.User',
        on_delete=models.CASCADE,
    )
    game = models.ForeignKey(
        verbose_name='Игра',
        to='Game',
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


class GamePayment(models.Model):
    """Class that represents user payment for the game"""

    class Meta:
        verbose_name = 'Платеж пользователя'
        verbose_name_plural = 'Платежи пользователей'

    identifier = models.CharField(
        verbose_name='Идентификатор',
        max_length=255,
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    game = models.ForeignKey(
        verbose_name='Игра',
        to='Game',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    coupon = models.ForeignKey(
        verbose_name='Купон',
        to='coupons.Coupon',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    summa = models.DecimalField(
        verbose_name='Сумма',
        max_digits=12,
        decimal_places=2,
    )
    discount = models.DecimalField(
        verbose_name='Скидка',
        max_digits=12,
        decimal_places=2,
    )
    discount_units = models.CharField(
        verbose_name='Удиницы измирения',
        max_length=10,
    )
    summa_with_discount = models.DecimalField(
        verbose_name='Сумма со скидкой',
        max_digits=12,
        decimal_places=2,
    )
    currency = models.CharField(
        verbose_name='Валюта',
        max_length=10,
    )
    places_count = models.IntegerField(
        verbose_name='Количество оплаченных мест',
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=255,
        choices=PAYMENT_STATUSES,
        default='PENDING',
    )
    cancel_message = models.CharField(
        verbose_name='Причина отмены',
        max_length=255,
        default='',
        blank=True,
    )

    def __str__(self):
        return self.identifier


class GamePaymentRefund(models.Model):
    """Class that represents user payment refund for the game"""

    class Meta:
        verbose_name = 'Возврат платежа пользователя'
        verbose_name_plural = 'Возвраты платежей пользователей'

    identifier = models.CharField(
        verbose_name='Идентификатор',
        max_length=255,
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=10,
        choices=REFUND_STATUSES,
    )
    value = models.DecimalField(
        verbose_name='Сумма',
        max_digits=12,
        decimal_places=2,
    )
    currency = models.CharField(
        verbose_name='Валюта',
        max_length=10,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
    )
    payment = models.ForeignKey(
        verbose_name='Платеж',
        to='games.GamePayment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    game = models.ForeignKey(
        verbose_name='Игра',
        to='Game',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.identifier


class GamePlayerEvaluation(models.Model):
    """Class that represents a player evaluation for a game"""

    class Meta:
        verbose_name = 'Оценка участника'
        verbose_name_plural = 'Оценки участников'

    game = models.ForeignKey(
        verbose_name='Игра',
        to='Game',
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
