from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, DateFromToRangeFilter
from business.models import Contract


class ContractFilter(FilterSet):
    class Meta:
        model = Contract
        fields = {
            "client__last_name": ["exact"],
            "client__email": ["exact"],
            "amount": ["lt", "gt"],
            "date_created": ["exact", "year__lt", "year__gt", "month__lt", "month__gt"],
        }


class RangeAmountListFilter(SimpleListFilter):
    title = _("amount")
    parameter_name = "amount"

    def lookups(self, request, model_admin):
        return (
            ("0-1000", _("Entre 0 et 1000 euros.")),
            ("1000-10000", _("Entre 1000 et 10k euros.")),
            ("10000-50000", _("Entre 10k et 50k euros.")),
            ("50000-100000", _("Entre 50k et 100k euros.")),
            ("100000-x", _("Plus de 100k euros.")),
        )

    def queryset(self, request, queryset):
        if self.value() == "0-1000":
            return queryset.filter(
                amount__lte=1000,
            )
        if self.value() == "1000-10000":
            return queryset.filter(
                amount__gte=1000,
                amount__lte=10000,
            )
        if self.value() == "10000-50000":
            return queryset.filter(
                amount__gte=10000,
                amount__lte=50000,
            )
        if self.value() == "50000-100000":
            return queryset.filter(
                amount__gte=50000,
                amount__lte=100000,
            )
        if self.value() == "100000-x":
            return queryset.filter(
                amount__gte=100000,
            )
