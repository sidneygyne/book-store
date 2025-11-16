from rest_framework import viewsets
from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
