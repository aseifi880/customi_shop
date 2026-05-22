from rest_framework import serializers

from stores.models import Store, Product, Category


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all(),
    )

    class Meta:
        model = Category
        fields = ("name", "products")


class ProductRetrieveSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.BigIntegerField()
    image = serializers.ImageField(use_url=True)
    stock = serializers.IntegerField()
    category = serializers.HyperlinkedRelatedField(
        view_name="category-detail",
        queryset=Category.objects.all(),
    )
    in_stock = serializers.SerializerMethodField(method_name="get_in_stock")

    def get_in_stock(self, obj):
        return obj.in_stock()

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "image",
            "stock",
            "category",
            "price",
            "in_stock",
        ]


class StoreSerializer(serializers.ModelSerializer):
    products = ProductRetrieveSerializer(many=True)

    class Meta:
        model = Store
        fields = ["name", "description", "address", "owner", "created_at"]
        read_only_fields = ["created_at", "owner"]
