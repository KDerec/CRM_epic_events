from django.contrib import admin
from django.urls import path
from business.admin import crm_admin_site

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", crm_admin_site.urls),
]
