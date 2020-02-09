# Generated by Django 2.2.5 on 2020-02-09 21:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(max_length=15, unique=True, verbose_name='Номер телефона')),
                ('phone_activation_code', models.IntegerField(blank=True, default=None, null=True, verbose_name='Последний код активации номера телефона')),
                ('is_active_phone', models.BooleanField(default=False, verbose_name='Номер телефона подтвержден')),
                ('username', models.CharField(blank=True, default='', max_length=255, verbose_name='Логин')),
                ('first_name', models.CharField(blank=True, default='', max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, default='', max_length=255, verbose_name='Фамилия')),
                ('birthday_date', models.DateField(blank=True, default=None, null=True, verbose_name='Дата рождения')),
                ('gender', models.CharField(choices=[('NOT_SET', 'Не установлена'), ('MALE', 'Мужчина'), ('FEMALE', 'Женщина')], default='NOT_SET', max_length=255, verbose_name='Пол')),
                ('location', models.CharField(blank=True, default='', max_length=255, verbose_name='Локация')),
                ('reliability', models.DecimalField(blank=True, decimal_places=2, default=100, max_digits=5, verbose_name='Надежность')),
                ('profile_image', models.ImageField(blank=True, default=None, null=True, upload_to='images/profile_images', verbose_name='Фото профиля')),
                ('about', models.TextField(blank=True, default='', max_length=1000, verbose_name='Про себя')),
                ('active', models.BooleanField(default=True, verbose_name='Активный')),
                ('staff', models.BooleanField(default=False, verbose_name='Персонал')),
                ('admin', models.BooleanField(default=False, verbose_name='Администратор')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['id'],
            },
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подписка на пользователя',
                'verbose_name_plural': 'Подписки на пользователей',
            },
        ),
    ]
