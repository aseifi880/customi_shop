from rest_framework.generics import ListAPIView

from stores.models import Product, Category
from stores.serializers import ProductRetrieveSerializer, CategorySerializer


# Create your views here.
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer