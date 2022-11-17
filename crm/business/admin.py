from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.contrib.auth.models import Group
from business.models import Client, Event, Contract


class CrmAdminSite(admin.AdminSite):
    site_header = "Epic Events CRM"
    site_title = "Epic Events CRM"
    index_title = "Welcome to Epic Events CRM"


class ClientAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", "date_updated")

    def has_change_permission(self, request, obj=None):
        return can_change_object(self, request, obj)


def has_superuser_permission(request):
    return request.user.is_active and request.user.is_superuser


def can_change_object(self, request, obj):
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
crm_admin_site.register(Event)
crm_admin_site.register(Contract)
crm_admin_site.register(Group)

admin.site.has_permission = has_superuser_permission

admin.site.register(Client)
admin.site.register(Event)
admin.site.register(Contract)
