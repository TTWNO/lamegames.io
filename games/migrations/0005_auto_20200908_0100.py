# Generated by Django 3.1 on 2020-09-08 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_auto_20200908_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activeuser',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='activeuser',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='active_users', to='games.room'),
        ),
    ]
