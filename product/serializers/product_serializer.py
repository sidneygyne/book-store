from rest_framework import serializers
from product.models import Category, Product
from product.serializers.category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    # leitura: mostra as categorias associadas
    category = CategorySerializer(read_only=True, many=True, source="categories")

    # escrita: permite enviar lista de IDs de categorias
    categories_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, many=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "active",
            "category",  # leitura (nested serializer)
            "categories_id",  # escrita (lista de IDs)
        ]

    def create(self, validated_data):
        category_data = validated_data.pop("categories_id", [])
        product = Product.objects.create(**validated_data)
        if category_data:
            product.categories.set(category_data)
        return product

    def update(self, instance, validated_data):
        category_data = validated_data.pop("categories_id", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if category_data is not None:
            instance.categories.set(category_data)
        return instance
