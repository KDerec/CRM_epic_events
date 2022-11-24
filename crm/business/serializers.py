from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import serializers
from business.models import Client, Contract, Event


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = [
            "url",
            "first_name",
            "last_name",
            "email",
            "phone",
            "mobile",
            "company_name",
            "date_created",
            "date_updated",
            "sales_contact",
        ]

    def is_valid(self, *, raise_exception=False):
        try:
            self.initial_data["sales_contact"]
        except MultiValueDictKeyError:
            return super().is_valid(raise_exception=raise_exception)
        self.initial_data._mutable = True
        self.initial_data.pop("sales_contact")
        return super().is_valid(raise_exception=raise_exception)


class ClientSerializerForSales(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = [
            "url",
            "first_name",
            "last_name",
            "email",
            "phone",
            "mobile",
            "company_name",
            "date_created",
            "date_updated",
            "sales_contact",
        ]
        extra_kwargs = {
            "sales_contact": {"read_only": True},
        }


class ContractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "url",
            "status",
            "amount",
            "payment_due",
            "client",
            "sales_contact",
            "event",
        ]

    def is_valid(self, *, raise_exception=False):
        try:
            self.initial_data["sales_contact"]
            self.initial_data["client"]
            self.initial_data["event"]
        except MultiValueDictKeyError:
            return super().is_valid(raise_exception=raise_exception)
        self.initial_data._mutable = True
        self.initial_data.pop("sales_contact")
        self.initial_data.pop("client")
        self.initial_data.pop("event")
        return super().is_valid(raise_exception=raise_exception)


class ContractSerializerForSales(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "url",
            "status",
            "amount",
            "payment_due",
            "client",
            "sales_contact",
            "event",
        ]
        extra_kwargs = {
            "sales_contact": {"read_only": True},
        }

    def is_valid(self, *, raise_exception=False):
        try:
            self.initial_data["client"]
            self.initial_data["event"]
        except MultiValueDictKeyError:
            return super().is_valid(raise_exception=raise_exception)
        self.initial_data._mutable = True
        self.initial_data.pop("client")
        self.initial_data.pop("event")
        return super().is_valid(raise_exception=raise_exception)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = [
            "url",
            "event_status",
            "attendees",
            "event_date",
            "notes",
            "client",
            "support_contact",
        ]

    def is_valid(self, *, raise_exception=False):
        try:
            self.initial_data["client"]
            self.initial_data["support_contact"]
        except MultiValueDictKeyError:
            return super().is_valid(raise_exception=raise_exception)
        self.initial_data._mutable = True
        self.initial_data.pop("client")
        self.initial_data.pop("support_contact")
        return super().is_valid(raise_exception=raise_exception)


class EventSerializerForSupport(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = [
            "url",
            "event_status",
            "attendees",
            "event_date",
            "notes",
            "client",
            "support_contact",
        ]
        extra_kwargs = {
            "support_contact": {"read_only": True},
            "client": {"read_only": True},
        }
