from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from business.admin import crm_admin_site
from accounts.views import UserViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("", crm_admin_site.urls),
]
