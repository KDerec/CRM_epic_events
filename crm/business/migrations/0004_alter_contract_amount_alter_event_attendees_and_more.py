# Generated by Django 4.1.2 on 2022-11-12 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("business", "0003_alter_contract_event_alter_contract_payment_due"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contract",
            name="amount",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="event",
            name="attendees",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="event",
            name="event_date",
            field=models.DateField(),
        ),
    ]
