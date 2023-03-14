# Generated by Django 4.1.4 on 2023-03-12 19:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mov', '0022_season_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='trailer',
            field=models.FileField(upload_to='videos/trailers/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mov', 'avi', 'mp4', 'webm', 'mkv', 'vbmv'])]),
        ),
        migrations.AlterField(
            model_name='series',
            name='trailer',
            field=models.FileField(upload_to='videos/trailers/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mov', 'avi', 'mp4', 'webm', 'mkv', 'vbmv'])]),
        ),
    ]