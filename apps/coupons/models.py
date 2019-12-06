from django.db import models

from users.models import User

COUPON_UNITS = [
    ('PERCENT', '%'),
    ('RUB', 'RUB'),
]

COUPON_TYPES = [
    ('INDIVIDUAL', 'Индивидуальный'),
    ('GENERAL', 'Общий'),
]


class Coupon(models.Model):
    """Class that represents coupon"""

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    code = models.CharField(
        verbose_name='Код',
        max_length=10,
    )
    start_date = models.DateField(
        verbose_name='Начало действия',
    )
    end_date = models.DateField(
        verbose_name='Окончание действия',
    )
    discount = models.DecimalField(
        verbose_name='Скидка',
        decimal_places=2,
        max_digits=12,
    )
    units = models.CharField(
        verbose_name='Единицы измерения',
        max_length=7,
        choices=COUPON_UNITS,
    )
    type = models.CharField(
        verbose_name='Тип',
        max_length=15,
        choices=COUPON_TYPES,
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
    )
