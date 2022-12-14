# Generated by Django 4.1.2 on 2022-10-19 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_remove_user_team"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="team",
            field=models.CharField(
                choices=[
                    ("Management", "Management"),
                    ("Sales", "Sales"),
                    ("Support", "Support"),
                ],
                default="Support",
                help_text="Choisir l'équipe de cet employé.",
                max_length=10,
            ),
        ),
    ]
