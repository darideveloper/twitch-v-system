# Generated by Django 4.0.4 on 2023-08-14 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_alter_commentphantom_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='commenthistory',
            name='comment_phantom',
        ),
        migrations.AddField(
            model_name='comment',
            name='category',
            field=models.CharField(default='', max_length=200, verbose_name='Comentario del mod'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='comments',
            field=models.TextField(default='', verbose_name='Comentarios posibles de bot (uno por línea)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commenthistory',
            name='comment_bot',
            field=models.CharField(default='', max_length=200, verbose_name='Comentario de bot'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commenthistory',
            name='comment_mod',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='comments.comment', verbose_name='Comentario'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CommentPhantom',
        ),
    ]
