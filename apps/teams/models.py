from django.db import models

from users.models import POSITIONS

NUMBER_OF_PLAYERS_PER_TEAM = [
    ('5', '5 со стороны'),
    ('6', '6 со стороны'),
    ('7', '7 со стороны'),
    ('8', '8 со стороны'),
    ('9', '9 со стороны'),
    ('10', '10 со стороны'),
    ('11', '11 со стороны'),
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
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    players_count_per_team = models.CharField(
        verbose_name='Количество игроков в команде',
        max_length=255,
        choices=NUMBER_OF_PLAYERS_PER_TEAM,
    )

    def __str__(self):
        return '{}'.format(self.name)


class UserInTeam(models.Model):
    """Class that represents user in a team"""

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
        to='teams.Team',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name='Игрок',
        to='users.User',
        on_delete=models.CASCADE,
    )
    user_position = models.CharField(
        verbose_name='Позиция',
        max_length=255,
        choices=POSITIONS,
    )

    def __str__(self):
        return '{} - {} {}'.format(self.user.username, self.game.title, self.team.name)


class ReservedPlaceInTeam(models.Model):
    """Class that represents reserved place in a team by user for another gamer"""

    class Meta:
        verbose_name = 'Забронированное место в команде'
        verbose_name_plural = 'Забронированные места в команде'

    game = models.ForeignKey(
        verbose_name='Игра',
        to='games.Game',
        on_delete=models.CASCADE,
    )
    team = models.ForeignKey(
        verbose_name='Команда',
        to='teams.Team',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name='Кто забронировал место',
        to='users.User',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    reserved_position = models.CharField(
        verbose_name='Позиция',
        max_length=255,
        choices=POSITIONS,
    )

    def __str__(self):
        return '{} - {} {}'.format(self.title, self.game.title, self.team.name)
