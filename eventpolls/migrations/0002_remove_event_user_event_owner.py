# Generated by Django 4.2.3 on 2023-07-23 17:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("eventpolls", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="user",
        ),
        migrations.AddField(
            model_name="event",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]