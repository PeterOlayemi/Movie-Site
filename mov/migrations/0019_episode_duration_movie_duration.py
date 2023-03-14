# Generated by Django 4.1.4 on 2023-03-12 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mov', '0018_remove_episode_duration_remove_movie_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='duration',
            field=models.CharField(default='00:00:00', max_length=8),
        ),
        migrations.AddField(
            model_name='movie',
            name='duration',
            field=models.CharField(default='00:00:00', max_length=8),
        ),
    ]
