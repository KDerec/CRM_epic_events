from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User
from business.admin import crm_admin_site

crm_admin_site.register(User, UserAdmin)
admin.site.register(User, UserAdmin)
