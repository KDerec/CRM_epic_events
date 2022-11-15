from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from business.admin import crm_admin_site


class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "groupes",
        "is_staff",
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "groups"),
            },
        ),
    )

    def groupes(self, obj):
        try:
            return obj.groups.get()
        except:
            return "N/A"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # exclude admin
        return qs.exclude(id=1)


crm_admin_site.register(User, UserAdmin)
admin.site.register(User, UserAdmin)
