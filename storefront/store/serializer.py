from rest_framework import serializers
from decimal import Decimal
from store.models import Product
from store.models import Collection

class CollectionSerializer(serializers.Serializer):
     id = serializers.IntegerField()


# django-rest-framework.org-->api guide
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=225)
    price = serializers.DecimalField(max_digits=6, decimal_places=2 , source = 'unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()
    collection = serializers.HyperlinkedRelatedField(
        queryset = Collection.objects.all(),
        view_name='collection-detail',
    )
    def calculate_tax(self,product: Product):
        return product.unit_price * Decimal(1.1)
