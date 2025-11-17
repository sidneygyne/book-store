import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from order.models.order import Order
from product.models.product import Product

@pytest.mark.django_db
def test_order_create_viewset():
    client = APIClient()

    # cria usuário e token de autenticação
    user = User.objects.create_user(username="sidney", password="123456")
    token = Token.objects.create(user=user)

    # adiciona token no header para autenticação via TokenAuthentication
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    # cria dois produtos que serão adicionados ao pedido
    product1 = Product.objects.create(title="Livro 1", price=30, active=True)
    product2 = Product.objects.create(title="Livro 2", price=70, active=True)

    # payload enviado para criar o pedido
    payload = {
        "user": user.id,                # id do usuário dono do pedido
        "product": [product1.id, product2.id],  # lista de produtos no pedido
    }

    # faz requisição POST para criar o pedido
    response = client.post("/api/orders/", payload, format="json")

    # valida que o pedido foi criado com sucesso
    assert response.status_code == 201

    # valida dados retornados pela API
    data = response.json()
    assert data["total"] == 100              # soma dos preços dos produtos