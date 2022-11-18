from django.db import models
from accounts.models import User


class Client(models.Model):
    """Client model."""

    client_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.first_name} {self.last_name} de {self.company_name}"


class Event(models.Model):
    """Event model."""

    event_id = models.BigAutoField(primary_key=True)
    event_status = models.BooleanField(help_text="Si événement terminé, à cocher.")
    attendees = models.PositiveIntegerField()
    event_date = models.DateField()
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    support_contact = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        """String for representing the Model object."""
        return f"Event #{self.event_id} pour {self.client} le {self.event_date}"


class Contract(models.Model):
    """Contract model."""

    contract_id = models.BigAutoField(primary_key=True)
    status = models.BooleanField(help_text="Si contrat signé, à cocher.")
    amount = models.PositiveIntegerField()
    payment_due = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sales_contact = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        """String for representing the Model object."""
        return f"Contrat #{self.contract_id} pour {self.client} à payer le {self.payment_due}"
