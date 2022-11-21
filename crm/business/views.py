from rest_framework import viewsets
from accounts.permissions import MyDjangoModelPermissions
from business.models import Client, Contract, Event
from business.serializers import (
    ClientSerializer,
    ListClientSerializer,
    ContractSerializer,
    EventSerializer,
)


class ClientViewSet(viewsets.ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [MyDjangoModelPermissions]

    def get_serializer_class(self):
        try:
            self.kwargs["pk"]
            return super().get_serializer_class()
        except KeyError:
            return ListClientSerializer


class ContractViewSet(viewsets.ModelViewSet):

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [MyDjangoModelPermissions]


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [MyDjangoModelPermissions]
