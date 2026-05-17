from rest_framework import serializers

from stores.models import Store, Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class ProductRetrieveSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.BigIntegerField()
    image = serializers.ImageField(use_url=True)
    stock = serializers.IntegerField()
    category = CategorySerializer()
    in_stock = serializers.BooleanField()

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'stock', 'category', 'in_stock']


class StoreSerializer(serializers.ModelSerializer):
    products =  ProductRetrieveSerializer(many=True)

    class Meta:
        model = Store
        fields = ['name', 'description', 'address', 'owner', 'created_at']
        read_only_fields = ['created_at', 'owner']
