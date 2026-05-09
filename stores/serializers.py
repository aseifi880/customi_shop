from rest_framework import serializers

from stores.models import Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['name', 'description', 'address', 'owner', 'created_at']
        read_only_fields = ['created_at', 'owner']


