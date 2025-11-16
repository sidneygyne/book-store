import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from product.models.product import Product
from product.models.category import Category

@pytest.mark.django_db
def test_product_list_viewset():
    client = APIClient()

    # cria usuário e autentica
    user = User.objects.create_user(username="sidney", password="123456")
    client.force_authenticate(user=user)

    # cria dados
    category = Category.objects.create(title="Romance", slug="romance")
    product = Product.objects.create(title="Livro A", price=50, active=True)
    product.categories.add(category)

    # faz requisição GET
    response = client.get("/api/products/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Livro A"
    assert data[0]["category"][0]["title"] == "Romance"


@pytest.mark.django_db
def test_product_create_viewset():
    client = APIClient()
    user = User.objects.create_user(username="sidney", password="123456")
    client.force_authenticate(user=user)

    payload = {
        "title": "Livro B",
        "description": "Novo livro",
        "price": 100,
        "active": True,
    }

    response = client.post("/api/products/", payload, format="json")

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Livro B"
    assert data["price"] == 100
    assert data["active"] is True
