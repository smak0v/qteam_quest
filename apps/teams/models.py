from django.db import models

PAYMENT_STATUSES = [
    ('PENDING', 'Pending'),
    ('WAITING_FOR_CAPTURE', 'Waiting for capture'),
    ('SUCCEEDED', 'Succeeded'),
    ('CANCELED', 'Canceled'),
]

REFUND_STATUSES = [
    ('SUCCEEDED', 'Succeeded'),
]


class Team(models.Model):
    """Class that represents the team"""

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    game = models.ForeignKey(
        verbose_name='Игра',
        to='games.Game',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.game.title}'


class UserInTeam(models.Model):
    """Class that represents user in a team after payment of all reserved places"""

    class Meta:
        verbose_name = 'Игрок в команде'
        verbose_name_plural = 'Игроки в команде'

    game = models.ForeignKey(
        verbose_name='Игра',
        to='games.Game',
        on_delete=models.CASCADE,
    )
    team = models.ForeignKey(
        verbose_name='Команда',
        to='Team',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='users.User',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=255,
        default=None,
        null=True,
        blank=True,
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=255,
        choices=PAYMENT_STATUSES,
        default='PENDING',
    )

    def __str__(self):
        return f'{self.game.title} - {self.user.username} - {self.title}'


class TemporaryReserve(models.Model):
    """Class that represents temporary reserve (5 minutes) of one place in team for the game"""

    class Meta:
        verbose_name = 'Временный резерв'
        verbose_name_plural = 'Временные резервы'

    game = models.ForeignKey(
        verbose_name='Игра',
        to='games.Game',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name='Кто забронировал место',
        to='users.User',
        on_delete=models.CASCADE,
    )
    timespan = models.DateTimeField(
        verbose_name='Время создания резерва',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.game.title} - {self.user.phone}'
