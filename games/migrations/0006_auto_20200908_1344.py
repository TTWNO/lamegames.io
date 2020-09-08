# Generated by Django 3.1 on 2020-09-08 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_auto_20200908_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='game_name',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activeuser',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
