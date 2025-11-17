from rest_framework import serializers
from order.models.order import Order
from product.models.product import Product


class OrderSerializer(serializers.ModelSerializer):
    # aceita lista de IDs de produtos no POST/PUT
    product = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )
    # calcula o total dinamicamente
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "user", "product", "total"]

    def get_total(self, obj):
        # soma os preços de todos os produtos associados
        return sum(p.price for p in obj.product.all())

    def create(self, validated_data):
        products = validated_data.pop("product", [])
        order = Order.objects.create(**validated_data)
        order.product.set(products)
        return order

    def update(self, instance, validated_data):
        products = validated_data.pop("product", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if products is not None:
            instance.product.set(products)
        return instance
