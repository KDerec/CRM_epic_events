from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.contrib.auth.models import Group
from business.models import Client, Event, Contract
from business.filters import RangeAmountListFilter
from accounts.models import User


class CrmAdminSite(admin.AdminSite):
    site_header = "Epic Events CRM"
    site_title = "Epic Events CRM"
    index_title = "Welcome to Epic Events CRM"


class ClientAdmin(admin.ModelAdmin):
    list_display = ("__str__", "sales_contact")
    list_filter = (
        "email",
        "last_name",
    )
    readonly_fields = ("date_created", "date_updated")

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name="Sales").exists():
            if "sales_contact" not in self.readonly_fields:
                self.readonly_fields += ("sales_contact",)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not request.user.groups.filter(name="Manager").exists():
            obj.sales_contact = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return can_change_object(self, request, obj)


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "event_id",
        "client",
        "event_date",
        "support_contact",
        "event_status",
    )
    list_filter = (
        "client__last_name",
        "client__email",
        "event_date",
    )
    readonly_fields = ("date_created", "date_updated")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.groups.filter(name="Sales").exists():
            if db_field.name == "client":
                kwargs["queryset"] = Client.objects.filter(sales_contact=request.user)
        if db_field.name == "support_contact":
            kwargs["queryset"] = User.objects.filter(groups__name__in=["Support"])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name="Support").exists():
            if "support_contact" not in self.readonly_fields:
                self.readonly_fields += ("support_contact",)
            if "client" not in self.readonly_fields:
                self.readonly_fields += ("client",)
        return self.readonly_fields

    def has_change_permission(self, request, obj=None):
        return can_change_object(self, request, obj)


class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "contract_id",
        "amount",
        "payment_due",
        "sales_contact",
        "event_id",
        "status",
    )
    list_filter = (
        RangeAmountListFilter,
        "client__last_name",
        "client__email",
        "date_created",
        "amount",
    )
    readonly_fields = ("date_created", "date_updated")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.groups.filter(name="Sales").exists():
            sales_user_client = Client.objects.filter(sales_contact=request.user)
            if db_field.name == "client":
                kwargs["queryset"] = sales_user_client
            if db_field.name == "event":
                kwargs["queryset"] = Event.objects.filter(client__in=sales_user_client)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name="Sales").exists():
            if "sales_contact" not in self.readonly_fields:
                self.readonly_fields += ("sales_contact",)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not request.user.groups.filter(name="Manager").exists():
            obj.sales_contact = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return can_change_object(self, request, obj)


def has_superuser_permission(request):
    return request.user.is_active and request.user.is_superuser


def can_change_object(self, request, obj):
    try:
        if (
            request.user.groups.filter(name="Sales").exists()
            and obj.client.sales_contact == request.user
        ):
            return True
        if (
            request.user.groups.filter(name="Sales").exists()
            and obj.client.sales_contact != request.user
        ):
            return False
    except:
        pass
    try:
        if request.user.groups.filter(name="Manager").exists():
            return True
    except AttributeError:
        pass
    try:
        if obj.sales_contact == request.user:
            return True
        else:
            return False
    except AttributeError:
        pass
    try:
        if obj.support_contact == request.user:
            return True
        else:
            return False
    except AttributeError:
        pass

    opts = self.opts
    codename = get_permission_codename("change", opts)
    return request.user.has_perm("%s.%s" % (opts.app_label, codename))


crm_admin_site = CrmAdminSite(name="crm_admin_site")

crm_admin_site.register(Client, ClientAdmin)
crm_admin_site.register(Event, EventAdmin)
crm_admin_site.register(Contract, ContractAdmin)
crm_admin_site.register(Group)

admin.site.has_permission = has_superuser_permission

admin.site.register(Client)
admin.site.register(Event)
admin.site.register(Contract)
