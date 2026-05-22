from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from stores.filters import ProductFilter, CategoryFilter
from stores.models import Product, Category, Store
from stores.serializers import (
    ProductRetrieveSerializer,
    CategorySerializer,
    StoreSerializer,
)


# Create your views here.
class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.prefetch_related("products").all()
    serializer_class = CategorySerializer


class CategoryListViewSet(ModelViewSet):
    queryset = Category.all_objects.prefetch_related("products").all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ProductListView(ListAPIView):
    filterset_class = ProductFilter
    search_fields = (
        "name",
        "description",
    )
    ordering_fields = ("name", "price")
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductRetrieveSerializer


class CategoryListView(ListAPIView):
    filterset_class = CategoryFilter
    search_fields = ("name",)
    ordering_fields = ("name",)
    queryset = Category.objects.prefetch_related("products").all()
    serializer_class = CategorySerializer


class StoreListView(ListAPIView):
    filterset_fields = ("name",)
    search_fields = ("name",)
    ordering_fields = ("name",)
    queryset = Store.objects.prefetch_related("products").all()
    serializer_class = StoreSerializer
