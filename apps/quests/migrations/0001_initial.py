# Generated by Django 2.2.5 on 2020-02-09 21:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('phone', models.CharField(max_length=15, verbose_name='Номер телефона')),
                ('description', models.CharField(blank=True, default='', max_length=100, verbose_name='Описание')),
                ('location', models.CharField(max_length=255, verbose_name='Локация')),
                ('x_coordinate', models.DecimalField(decimal_places=5, max_digits=7, verbose_name='Х координата')),
                ('y_coordinate', models.DecimalField(decimal_places=5, max_digits=7, verbose_name='У координата')),
                ('cover_image', models.ImageField(blank=True, default=None, null=True, upload_to='images/quest_covers', verbose_name='Обложка')),
                ('photo', models.ImageField(blank=True, default=None, null=True, upload_to='images/quest_photos', verbose_name='Фото')),
                ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='Рейтинг')),
            ],
            options={
                'verbose_name': 'Квест',
                'verbose_name_plural': 'Квесты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='QuestSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quests.Quest', verbose_name='Квест')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подписка на квест',
                'verbose_name_plural': 'Подписки на квесты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='QuestImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/quest_gallery', verbose_name='Фото')),
                ('uploading_timespan', models.DateTimeField(auto_now_add=True, verbose_name='Время загрузки')),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quests.Quest', verbose_name='Квест')),
            ],
            options={
                'verbose_name': 'Фото квеста',
                'verbose_name_plural': 'Фото квестов',
                'ordering': ['-uploading_timespan'],
            },
        ),
        migrations.CreateModel(
            name='QuestComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')),
                ('text', models.CharField(max_length=900, verbose_name='Комментарий')),
                ('scores', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1, verbose_name='Оценка')),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='quests.Quest', verbose_name='Квест')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Комментарий квеста',
                'verbose_name_plural': 'Комментарии квеста',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='MetroStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('color', models.CharField(max_length=7, verbose_name='Цвет ветки (в формате #FFFFFF)')),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metro_stations', to='quests.Quest', verbose_name='Квест')),
            ],
            options={
                'verbose_name': 'Станция метро',
                'verbose_name_plural': 'Станции метро',
                'ordering': ['id'],
            },
        ),
    ]
