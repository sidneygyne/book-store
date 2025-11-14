from rest_framework import serializers

from product.models import Category, Product

from product.serializers.category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True, source="categories")

    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "price",
            "active",
            "category",
        ]