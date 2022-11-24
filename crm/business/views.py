from django.http import Http404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS
from django.utils.datastructures import MultiValueDictKeyError
from accounts.permissions import MyDjangoModelPermissions
from accounts.models import User
from business.models import Client, Contract, Event
from business.serializers import (
    ClientSerializer,
    ClientSerializerForSales,
    ContractSerializer,
    ContractSerializerForSales,
    EventSerializer,
    EventSerializerForSupport,
)


class ClientViewSet(viewsets.ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [MyDjangoModelPermissions]

    def get_permissions(self):
        if self.detail is True and self.request.method not in SAFE_METHODS:
            try:
                client = Client.objects.get(client_id=self.kwargs["pk"])
                user = self.request.user
            except Client.DoesNotExist:
                raise Http404("Ce numéro de client n'existe pas.")
            if (
                user.groups.filter(name="Sales").exists()
                and client.sales_contact != user
            ):
                raise PermissionDenied
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.user.groups.filter(name="Sales").exists():
            return ClientSerializerForSales
        else:
            return super().get_serializer_class()

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
        save_serializer_for_client_object(self, serializer, sales_contact)

    def update(self, request, *args, **kwargs):
        try:
            sales_contact = request.data["sales_contact"]
        except MultiValueDictKeyError:
            sales_contact = "is_empty"
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, sales_contact)
        serializer.save()

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer, sales_contact):
        save_serializer_for_client_object(self, serializer, sales_contact)


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [MyDjangoModelPermissions]

    def get_permissions(self):
        if self.detail is True and self.request.method not in SAFE_METHODS:
            try:
                event = Event.objects.get(event_id=self.kwargs["pk"])
                user = self.request.user
            except Event.DoesNotExist:
                raise Http404("Ce numéro d'event n'existe pas.")
            if (
                user.groups.filter(name="Sales").exists()
                and event.client.sales_contact != user
            ):
                raise PermissionDenied
            if (
                user.groups.filter(name="Support").exists()
                and event.support_contact != user
            ):
                raise PermissionDenied
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.user.groups.filter(name="Support").exists():
            return EventSerializerForSupport
        else:
            return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        try:
            client = request.data["client"]
        except MultiValueDictKeyError:
            client = "is_empty"
        try:
            support_contact = request.data["support_contact"]
        except MultiValueDictKeyError:
            support_contact = "is_empty"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, client, support_contact)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, client, support_contact):
        save_serializer_for_event_object(self, serializer, client, support_contact)

    def update(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name="Support").exists():
            try:
                if request.data["client"]:
                    raise ValidationError("Vous ne pouvez pas modifier le client.")
            except MultiValueDictKeyError:
                pass
            try:
                if request.data["support_contact"]:
                    raise ValidationError(
                        "Vous ne pouvez pas modifier le support contact."
                    )
            except MultiValueDictKeyError:
                pass
            return super().update(request, *args, **kwargs)
        try:
            client = request.data["client"]
        except MultiValueDictKeyError:
            client = "is_empty"
        try:
            support_contact = request.data["support_contact"]
        except MultiValueDictKeyError:
            support_contact = "is_empty"
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, client, support_contact)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer, client=None, support_contact=None):
        if self.request.user.groups.filter(name="Support").exists():
            return super().perform_update(serializer)
        else:
            save_serializer_for_event_object(self, serializer, client, support_contact)


class ContractViewSet(viewsets.ModelViewSet):

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [MyDjangoModelPermissions]

    def get_permissions(self):
        if self.detail is True and self.request.method not in SAFE_METHODS:
            try:
                contract = Contract.objects.get(contract_id=self.kwargs["pk"])
                user = self.request.user
            except Contract.DoesNotExist:
                raise Http404("Ce numéro de contract n'existe pas.")
            if (
                user.groups.filter(name="Sales").exists()
                and contract.sales_contact != user
            ):
                raise PermissionDenied
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.user.groups.filter(name="Sales").exists():
            return ContractSerializerForSales
        else:
            return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        try:
            sales_contact = request.data["sales_contact"]
        except MultiValueDictKeyError:
            sales_contact = "is_empty"
        try:
            client = request.data["client"]
        except MultiValueDictKeyError:
            client = "is_empty"
        try:
            event = request.data["event"]
        except MultiValueDictKeyError:
            event = "is_empty"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, sales_contact, client, event)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, sales_contact, client, event):
        save_serializer_for_contract_object(
            self, serializer, sales_contact, client, event
        )

    def update(self, request, *args, **kwargs):
        try:
            sales_contact = request.data["sales_contact"]
        except MultiValueDictKeyError:
            sales_contact = "is_empty"
        try:
            client = request.data["client"]
        except MultiValueDictKeyError:
            client = "is_empty"
        try:
            event = request.data["event"]
        except MultiValueDictKeyError:
            event = "is_empty"
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, sales_contact, client, event)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer, sales_contact, client, event):
        save_serializer_for_contract_object(
            self, serializer, sales_contact, client, event
        )


def save_serializer_for_client_object(self, serializer, sales_contact):
    if self.request.user.groups.filter(name="Sales").exists():
        if sales_contact != "is_empty":
            raise ValidationError(
                "Vous ne pouvez pas modifier le champ 'sales_contact', veuillez le retirer de votre requête."
            )
        serializer.save(sales_contact=self.request.user)

    elif sales_contact == "is_empty":
        raise ValidationError("Veuillez renseigner un sales contact.")

    elif User.objects.filter(username=sales_contact).exists():
        serializer.save(sales_contact=User.objects.get(username=sales_contact))

    elif "http" in sales_contact:
        sales_contact_id = sales_contact.split("/")[-2]
        serializer.save(sales_contact=User.objects.get(id=sales_contact_id))

    else:
        raise ValidationError(
            "Veuillez renseigner un 'username' de 'sales contact' existant."
        )


def save_serializer_for_event_object(self, serializer, client, support_contact):
    if client == "is_empty":
        raise ValidationError("Veuillez renseigner un contract.")

    elif support_contact == "is_empty":
        raise ValidationError("Veuillez renseigner un support contact.")

    elif (
        User.objects.filter(username=support_contact).exists()
        and Client.objects.filter(email=client).exists()
    ):
        if (
            self.request.user.groups.filter(name="Sales").exists()
            and Client.objects.get(email=client).sales_contact != self.request.user
        ):
            raise ValidationError("Veuillez choisir un client qui vous appartient.")
        serializer.save(
            support_contact=User.objects.get(username=support_contact),
            client=Client.objects.get(email=client),
        )
    elif "http" in support_contact:
        support_contact_id = support_contact.split("/")[-2]
        client_id = client.split("/")[-2]
        serializer.save(
            support_contact=User.objects.get(id=support_contact_id),
            client=Client.objects.get(client_id=client_id),
        )
    else:
        try:
            Client.objects.get(email=client)
            User.objects.get(username=support_contact)
        except User.DoesNotExist:
            raise ValidationError(
                "Veuillez renseigner un 'username' de 'support contact' existant."
            )
        except Client.DoesNotExist:
            raise ValidationError(
                "Veuillez renseigner un 'email' de 'client' existant."
            )


def save_serializer_for_contract_object(self, serializer, sales_contact, client, event):

    if self.request.user.groups.filter(name="Sales").exists():
        if sales_contact != "is_empty":
            raise ValidationError(
                "Vous ne pouvez pas modifier le champ 'sales_contact', veuillez le retirer de votre requête."
            )
        elif client == "is_empty":
            raise ValidationError("Veuillez renseigner un client.")

        elif event == "is_empty":
            raise ValidationError("Veuillez renseigner un event.")
        try:
            int(event)
            client = Client.objects.get(email=client)
            event = Event.objects.get(event_id=event)
        except ValueError:
            raise ValueError("Veuillez renseigner un numéro d'id pour event.")
        except Client.DoesNotExist:
            raise ValidationError(
                "Veuillez renseigner un 'email' de 'client' existant."
            )
        except Event.DoesNotExist:
            raise ValidationError("Veuillez renseigner un 'id' de 'event' existant.")

        if client.sales_contact != self.request.user:
            raise ValidationError("Veuillez choisir un client qui vous appartient.")

        if event.client != client:
            raise ValidationError(
                "Veuillez choisir un event du même client que ce contrat."
            )
        else:
            serializer.save(
                sales_contact=self.request.user,
                client=client,
                event=event,
            )

    elif sales_contact == "is_empty":
        raise ValidationError("Veuillez renseigner un sales contact.")

    elif client == "is_empty":
        raise ValidationError("Veuillez renseigner un client.")

    elif event == "is_empty":
        raise ValidationError("Veuillez renseigner un event.")

    elif (
        User.objects.filter(username=sales_contact).exists()
        and Client.objects.filter(email=client).exists()
        and Event.objects.filter(event_id=event)
    ):
        serializer.save(
            sales_contact=User.objects.get(username=sales_contact),
            client=Client.objects.get(email=client),
            event=Event.objects.get(event_id=event),
        )

    elif "http" in sales_contact:
        sales_contact_id = sales_contact.split("/")[-2]
        client_id = client.split("/")[-2]
        event_id = event.split("/")[-2]
        serializer.save(
            sales_contact=User.objects.get(id=sales_contact_id),
            client=Client.objects.get(client_id=client_id),
            event=Event.objects.get(event_id=event_id),
        )

    else:
        try:
            int(event)
            User.objects.get(username=sales_contact)
            Client.objects.get(email=client)
            Event.objects.get(event_id=event)
        except ValueError:
            raise ValueError("Veuillez renseigner un numéro d'id pour event.")
        except User.DoesNotExist:
            raise ValidationError(
                "Veuillez renseigner un 'username' de 'sales contact' existant."
            )
        except Client.DoesNotExist:
            raise ValidationError(
                "Veuillez renseigner un 'email' de 'client' existant."
            )
        except Event.DoesNotExist:
            raise ValidationError("Veuillez renseigner un 'id' de 'event' existant.")
