# Generated by Django 3.1 on 2020-09-10 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0013_minesweepercell_flagged'),
    ]

    operations = [
        migrations.AddField(
            model_name='minesweepercell',
            name='game_over',
            field=models.BooleanField(default=False),
        ),
    ]
