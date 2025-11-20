import pytest
from order.models.order import Order
from product.models.product import Product
from product.models.category import Category
from order.serializers.order_serializer import OrderSerializer
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_order_serializer_total():
    user = User.objects.create_user(username="sidney", password="123456")
    order = Order.objects.create(user=user)

    product1 = Product.objects.create(title="Livro 1", price=30)
    product2 = Product.objects.create(title="Livro 2", price=70)
    order.product.set([product1, product2])

    serializer = OrderSerializer(order)
    data = serializer.data

    assert data["total"] == 100
    assert len(data["product"]) == 2
