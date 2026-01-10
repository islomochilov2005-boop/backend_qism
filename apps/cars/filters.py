from django_filters import rest_framework as filters
from .models import Mashina


class MashinaFilter(filters.FilterSet):
    marka = filters.CharFilter(lookup_expr='icontains')
    model = filters.CharFilter(lookup_expr='icontains')
    yil_min = filters.NumberFilter(field_name='yil', lookup_expr='gte')
    yil_max = filters.NumberFilter(field_name='yil', lookup_expr='lte')
    narx_min = filters.NumberFilter(field_name='narx', lookup_expr='gte')
    narx_max = filters.NumberFilter(field_name='narx', lookup_expr='lte')

    class Meta:
        model = Mashina
        fields = ['marka', 'model', 'ahvol', 'viloyat']
