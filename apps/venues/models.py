from django.db import models

from qteam_quest.settings import AUTH_USER_MODEL

VENUE_SCORES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]


class Venue(models.Model):
    """Class that represents the game venue"""

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    location = models.CharField(
        verbose_name='Локация (адрес)',
        max_length=255,
    )
    x_coordinate = models.DecimalField(
        verbose_name='Х координата',
        decimal_places=5,
        max_digits=7,
    )
    y_coordinate = models.DecimalField(
        verbose_name='У координата',
        decimal_places=5,
        max_digits=7,
    )
    cover_image = models.ImageField(
        verbose_name='Обложка',
        upload_to='images/venue_covers',
        null=True,
        default=None,
        blank=True,
    )
    photo = models.ImageField(
        verbose_name='Фото площадки',
        upload_to='images/venue_photos',
        null=True,
        default=None,
        blank=True,
    )
    rating = models.DecimalField(
        verbose_name='Рейтинг',
        decimal_places=2,
        max_digits=3,
        default=0,
    )

    def __str__(self):
        return '{}'.format(self.name)


class VenueComment(models.Model):
    """Class that represents comment for game venue"""

    class Meta:
        verbose_name = 'Комментарий площадки'
        verbose_name_plural = 'Комментарии площадки'

    venue = models.ForeignKey(
        verbose_name='Площадка',
        to='venues.Venue',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=AUTH_USER_MODEL,
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
    scores = models.CharField(
        verbose_name='Оценка',
        max_length=1,
        choices=VENUE_SCORES,
    )

    def __str__(self):
        return '{} : {}'.format(self.user.username, self.scores)


class VenueSubscription(models.Model):
    """Class that represents venue subscription by user"""

    class Meta:
        verbose_name = 'Подписка на площадку'
        verbose_name_plural = 'Подписки на площадки'

    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='users.User',
        on_delete=models.CASCADE,
        related_name='users',
    )
    venue = models.ForeignKey(
        verbose_name='Площадка',
        to='venues.Venue',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.venue.name)


class MetroStation(models.Model):
    """Class that represents metro station"""

    class Meta:
        verbose_name = 'Станция метро'
        verbose_name_plural = 'Станции метро'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    color = models.CharField(
        verbose_name='Цвет ветки (в формате #FFFFFF)',
        max_length=7,
    )
    venue = models.ForeignKey(
        verbose_name='Площадка',
        to='Venue',
        related_name='metro_stations',
        on_delete=models.CASCADE,
    )
