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
        return f"{self.client_id}, {self.first_name}, {self.last_name}"


class Event(models.Model):
    """Event model."""

    event_id = models.BigAutoField(primary_key=True)
    event_status = models.BooleanField(help_text="Si événement terminé, à cocher.")
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    support_contact = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.event_id}, {self.event_date}"


class Contract(models.Model):
    """Contract model."""

    contract_id = models.BigAutoField(primary_key=True)
    status = models.BooleanField(help_text="Si contrat signé, à cocher.")
    amount = models.FloatField()
    payment_due = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sales_contact = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.contract_id}, {self.payment_due}"
