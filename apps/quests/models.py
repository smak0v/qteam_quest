from django.db import models

from qteam_quest.settings import AUTH_USER_MODEL

QUEST_SCORES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]


class Quest(models.Model):
    """Class that represents the quests"""

    class Meta:
        verbose_name = 'Квест'
        verbose_name_plural = 'Квесты'
        ordering = [
            'id',
        ]

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=100,
        blank=True,
        default='',
    )
    location = models.CharField(
        verbose_name='Локация',
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
        upload_to='images/quest_covers',
        null=True,
        default=None,
        blank=True,
    )
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to='images/quest_photos',
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


class QuestImage(models.Model):
    """Class that represents a quest image"""

    class Meta:
        verbose_name = 'Фото квеста'
        verbose_name_plural = 'Фото квестов'
        ordering = [
            '-uploading_timespan',
        ]

    quest = models.ForeignKey(
        verbose_name='Квест',
        to='Quest',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='images/quest_gallery',
    )
    uploading_timespan = models.DateTimeField(
        verbose_name='Время загрузки',
        auto_now_add=True,
    )


class QuestComment(models.Model):
    """Class that represents comment for quests"""

    class Meta:
        verbose_name = 'Комментарий квеста'
        verbose_name_plural = 'Комментарии квеста'
        ordering = [
            '-timestamp',
        ]

    quest = models.ForeignKey(
        verbose_name='Квест',
        to='Quest',
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
        choices=QUEST_SCORES,
    )

    def __str__(self):
        return f'{self.user.phone} : {self.scores}'


class QuestSubscription(models.Model):
    """Class that represents quests subscription by user"""

    class Meta:
        verbose_name = 'Подписка на квест'
        verbose_name_plural = 'Подписки на квесты'
        ordering = [
            'id',
        ]

    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='users.User',
        on_delete=models.CASCADE,
        related_name='users',
    )
    quest = models.ForeignKey(
        verbose_name='Квест',
        to='Quest',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user.phone} - {self.quest.name}'


class MetroStation(models.Model):
    """Class that represents metro station"""

    class Meta:
        verbose_name = 'Станция метро'
        verbose_name_plural = 'Станции метро'
        ordering = [
            'id',
        ]

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    color = models.CharField(
        verbose_name='Цвет ветки (в формате #FFFFFF)',
        max_length=7,
    )
    quest = models.ForeignKey(
        verbose_name='Квест',
        to='Quest',
        related_name='metro_stations',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.name}-{self.color}'
