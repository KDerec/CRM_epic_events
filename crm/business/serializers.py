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


class ContractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
