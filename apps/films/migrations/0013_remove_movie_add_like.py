# Generated by Django 2.0.1 on 2018-05-12 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0012_auto_20180512_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='add_like',
        ),
    ]
