# Generated by Django 2.2.5 on 2019-12-11 21:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quests.Game', verbose_name='Игра')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
            },
        ),
        migrations.CreateModel(
            name='UserInTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quests.Game', verbose_name='Игра')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.Team', verbose_name='Команда')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Игрок')),
            ],
            options={
                'verbose_name': 'Игрок в команде',
                'verbose_name_plural': 'Игроки в команде',
            },
        ),
        migrations.CreateModel(
            name='ReservedPlaceInTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quests.Game', verbose_name='Игра')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.Team', verbose_name='Команда')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Кто забронировал место')),
            ],
            options={
                'verbose_name': 'Забронированное место в команде',
                'verbose_name_plural': 'Забронированные места в команде',
            },
        ),
    ]
