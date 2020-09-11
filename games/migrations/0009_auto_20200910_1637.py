# Generated by Django 3.1 on 2020-09-10 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0008_auto_20200910_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='activeuser',
            name='user',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='common.lameuser'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='minesweeperboard',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='games.activeuser'),
        ),
    ]