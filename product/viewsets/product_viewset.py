from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]  # público
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("id")
    
