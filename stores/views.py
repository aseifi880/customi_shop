from rest_framework.generics import ListAPIView

from stores.filters import ProductFilter, CategoryFilter
from stores.models import Product, Category, Store
from stores.serializers import ProductRetrieveSerializer, CategorySerializer, StoreSerializer


# Create your views here.
class ProductListView(ListAPIView):
    filterset_class = ProductFilter
    search_fields = ('name', 'description',)
    ordering_fields = ('name', 'price')
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer


class CategoryListView(ListAPIView):
    filterset_class = CategoryFilter
    search_fields = ('name',)
    ordering_fields = ('name',)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StoreListView(ListAPIView):
    filterset_fields = ('name', )
    search_fields = ('name',)
    ordering_fields = ('name',)
    queryset = Store.objects.prefetch_related('products').all()
    serializer_class = StoreSerializer
