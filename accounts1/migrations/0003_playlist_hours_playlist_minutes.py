# Generated by Django 4.1.4 on 2023-03-26 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_playlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="playlist", name="hours", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playlist", name="minutes", field=models.IntegerField(default=0),
        ),
    ]
