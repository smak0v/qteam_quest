# Generated by Django 2.2.5 on 2019-12-02 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userauthtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserChangePhone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15, verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'Изменение номера телефона',
                'verbose_name_plural': 'Изминение номеров телефонов',
            },
        ),
        migrations.CreateModel(
            name='UserChangePhoneConfirm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms_code', models.CharField(max_length=5, verbose_name='Код подтверждения')),
            ],
            options={
                'verbose_name': 'Подтверждение изменения номера телефона',
                'verbose_name_plural': 'Подтверждения изминений номеров телефонов',
            },
        ),
    ]
