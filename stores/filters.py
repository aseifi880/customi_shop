import django_filters

from stores.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Product

class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Category