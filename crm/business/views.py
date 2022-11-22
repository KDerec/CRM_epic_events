from rest_framework import viewsets
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.utils.datastructures import MultiValueDictKeyError
from accounts.permissions import MyDjangoModelPermissions
from accounts.models import User
from business.models import Client, Contract, Event
from business.serializers import (
    ClientSerializer,
    ContractSerializer,
    EventSerializer,
)


class ClientViewSet(viewsets.ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [MyDjangoModelPermissions]

    def create(self, request, *args, **kwargs):
        try:
            sales_contact = request.data["sales_contact"]
        except MultiValueDictKeyError:
            sales_contact = "is_empty"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, sales_contact)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, sales_contact):
        if sales_contact == "is_empty":
            raise ValidationError("Veuillez renseigner un sales contact.")

        if User.objects.filter(username=sales_contact).exists():
            client = serializer.save()
            client.sales_contact = User.objects.get(username=sales_contact)
            client.save()

        elif "http" in sales_contact:
            client = serializer.save()
            sales_contact_id = sales_contact.split("/")[-2]
            client.sales_contact = User.objects.get(id=sales_contact_id)
            client.save()
        else:
            raise ValidationError(
                "Veuillez renseigner un 'username' de 'sales contact' valide."
            )


class ContractViewSet(viewsets.ModelViewSet):

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [MyDjangoModelPermissions]


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [MyDjangoModelPermissions]
