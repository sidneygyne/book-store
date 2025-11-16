import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from order.models.order import Order
from product.models.product import Product

@pytest.mark.django_db
def test_order_create_viewset():
    client = APIClient()
    user = User.objects.create_user(username="sidney", password="123456")
    client.force_authenticate(user=user)

    product1 = Product.objects.create(title="Livro 1", price=30, active=True)
    product2 = Product.objects.create(title="Livro 2", price=70, active=True)

    payload = {
        "user": user.id,
        "product": [product1.id, product2.id],
    }

    response = client.post("/api/orders/", payload, format="json")

    assert response.status_code == 201
    data = response.json()
    assert data["total"] == 100
    assert len(data["product"]) == 2
