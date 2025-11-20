from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # ← público

    def get_queryset(self):
        return Category.objects.all().order_by("id")
