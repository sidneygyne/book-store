from rest_framework import serializers

from order.models import Order
from product.models import Product
from product.serializers.product_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        return sum([product.price for product in instance.product.all()])

    class Meta:
        model = Order
        fields = ["product", "total"]
