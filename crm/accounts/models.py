from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TEAM_CHOICES = [
        ("Management", "Management"),
        ("Sales", "Sales"),
        ("Support", "Support"),
    ]
    team = models.CharField(
        max_length=10,
        choices=TEAM_CHOICES,
        blank=True,
        help_text="Choisir l'équipe de cet employé.",
    )
