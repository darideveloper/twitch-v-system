# Generated by Django 4.0.4 on 2023-08-10 21:49

from django.db import migrations, models
import viwers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100, verbose_name='Usuario de bot')),
                ('password', models.CharField(max_length=100, verbose_name='Contraseña de bot')),
                ('cookies', models.JSONField(default=viwers.models.get_default_cookies, verbose_name='Cookies de bot')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
            ],
            options={
                'verbose_name': 'Bot',
                'verbose_name_plural': 'Bots',
            },
        ),
    ]