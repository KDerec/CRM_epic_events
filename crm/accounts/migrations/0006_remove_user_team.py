# Generated by Django 4.1.2 on 2022-10-26 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_alter_user_team"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="team",
        ),
    ]
