# Generated by Django 3.1 on 2020-08-24 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]
