# Generated by Django 4.2.6 on 2023-10-09 05:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='classification',
            field=models.CharField(default='A', max_length=4),
        ),
        migrations.AddField(
            model_name='person',
            name='bio',
            field=models.TextField(default='Text'),
        ),
        migrations.AddField(
            model_name='person',
            name='birth_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='character_name',
            field=models.CharField(default='Ex', max_length=128),
        ),
        migrations.AddField(
            model_name='person',
            name='gender',
            field=models.CharField(default='F/M', max_length=11),
        ),
        migrations.AddField(
            model_name='person',
            name='image_path',
            field=models.URLField(blank=True),
        ),
    ]
