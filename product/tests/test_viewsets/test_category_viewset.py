import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from product.models.category import Category


@pytest.mark.django_db
def test_category_list_viewset():
    client = APIClient()
    # dados
    Category.objects.create(title="Romance", slug="romance", description="Livros de romance", active=True)
    Category.objects.create(title="Ficção", slug="ficcao", description="Ficção científica", active=True)

    # GET
    response = client.get("/api/categories/")
    assert response.status_code == 200

    data = response.json()
    assert data["count"] == 2
    assert len(data["results"]) == 2
    assert {c["title"] for c in data["results"]} == {"Romance", "Ficção"}
    # confere estrutura
    for c in data["results"]:
        assert set(c.keys()) == {"title", "slug", "description", "active"}


@pytest.mark.django_db
def test_category_create_viewset():
    client = APIClient()

    payload = {
        "title": "Aventura",
        "slug": "aventura",
        "description": "Categorias de aventura",
        "active": True,
    }

    response = client.post("/api/categories/", payload, format="json")
    assert response.status_code == 201

    # valida registro criado
    cat = Category.objects.get(slug="aventura")
    assert cat.title == "Aventura"
    assert cat.active is True


@pytest.mark.django_db
def test_category_retrieve_viewset():
    client = APIClient()  # Definindo client aqui

    cat = Category.objects.create(title="Drama", slug="drama", description="Categoria dramática", active=True)

    response = client