# Generated by Django 3.1 on 2020-09-18 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0018_auto_20200911_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='minesweeperboard',
            name='bombs',
            field=models.SmallIntegerField(default=15),
        ),
        migrations.AddField(
            model_name='minesweeperboard',
            name='height',
            field=models.SmallIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='minesweeperboard',
            name='width',
            field=models.SmallIntegerField(default=10),
        ),
    ]
