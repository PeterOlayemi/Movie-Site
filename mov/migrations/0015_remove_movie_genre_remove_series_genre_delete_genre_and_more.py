# Generated by Django 4.1.4 on 2023-03-11 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mov', '0014_alter_episode_movie_alter_movie_genre_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='series',
            name='genre',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.CharField(default='Drama, Mystery', max_length=99),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='series',
            name='genre',
            field=models.CharField(default='Drama, Mystery', max_length=99),
            preserve_default=False,
        ),
    ]