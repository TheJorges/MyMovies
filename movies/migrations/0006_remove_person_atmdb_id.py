# Generated by Django 4.2.6 on 2023-10-23 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_person_atmdb_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='atmdb_id',
        ),
    ]