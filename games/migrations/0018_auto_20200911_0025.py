# Generated by Django 3.1 on 2020-09-11 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0017_auto_20200910_2346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activeuser',
            name='username',
        ),
        migrations.AlterField(
            model_name='minesweeperboard',
            name='status',
            field=models.IntegerField(choices=[(0, 'In Progress'), (1, 'Lost'), (2, 'Won')], default=0),
        ),
    ]
