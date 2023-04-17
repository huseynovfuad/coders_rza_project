import django_filters
from products.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lt")
    total_price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lt")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    total_price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")

    class Meta:
        model = Product
        fields = (
            "name", "price",
                  "price_max", "price_min",
                  "total_price_max", "total_price_min",
            "category__id", "category__name"
                  )