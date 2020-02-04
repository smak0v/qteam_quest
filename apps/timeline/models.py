from django.db import models

TIMELINE_BLOCK_TYPES = [
    ('GAME_MESSAGE', 'Сообщение связанное с игрой'),
    ('SIMPLE_MESSAGE', 'Простое сообщение'),
]


class TimelineBlock(models.Model):
    """Class that represents timeline block element"""

    class Meta:
        verbose_name = 'Элемент ленты'
        verbose_name_plural = 'Элементы ленты'

    def get_image(self):
        if self.image:
            return ROOT_URL + self.image.url

    type = models.CharField(
        verbose_name='Тип',
        max_length=255,
        choices=TIMELINE_BLOCK_TYPES,
    )
    timespan = models.DateTimeField(
        verbose_name='Дата и время',
        auto_now_add=True,
    )
    message = models.CharField(
        verbose_name='Сообщение',
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
        to='games.Game',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='images/timeline_images',
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return f'{self.type} {self.timespan} {self.message}'
