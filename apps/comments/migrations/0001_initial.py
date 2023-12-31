# Generated by Django 4.0.4 on 2023-08-07 18:28

import comments.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('streams', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100, verbose_name='Usuario de bot')),
                ('password', models.CharField(max_length=100, verbose_name='Contraseña de bot')),
                ('cookies', models.JSONField(default=comments.models.get_default_cookies, verbose_name='Cookies de bot')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
            ],
            options={
                'verbose_name': 'Bot',
                'verbose_name_plural': 'Bots',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=200, verbose_name='Comentario de bot o mod')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
            ],
            options={
                'verbose_name': 'Comentario de bots o mods',
                'verbose_name_plural': 'Comentarios de bots y mods',
            },
        ),
        migrations.CreateModel(
            name='Mod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=200, verbose_name='Usuario de moderador')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
            ],
            options={
                'verbose_name': 'Moderador',
                'verbose_name_plural': 'Moderadores',
            },
        ),
        migrations.CreateModel(
            name='CommentPhantom',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_res', models.CharField(max_length=200, verbose_name='Comentario de respuesta')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('comment_mod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.comment', verbose_name='Comentario de un mod')),
            ],
            options={
                'verbose_name': 'Comentario fantasma',
                'verbose_name_plural': 'Comentarios fantasma',
            },
        ),
        migrations.CreateModel(
            name='CommentHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now=True, verbose_name='Fecha y hora')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.bot', verbose_name='Bot')),
                ('comment_phantom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.commentphantom', verbose_name='Comentario fantasma')),
                ('mod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.mod', verbose_name='Moderador')),
                ('stream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streams.stream', verbose_name='Stream')),
            ],
            options={
                'verbose_name': 'Historial de comentarios',
                'verbose_name_plural': 'Historial de comentarios',
            },
        ),
    ]
