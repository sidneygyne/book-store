import pytest
from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer


@pytest.mark.django_db
def test_category_serializer_fields():
    category = Category.objects.create(
        title="Ficção", slug="ficcao", description="Livros de ficção", active=True
    )
    serializer = CategorySerializer(category)
    data = serializer.data

    assert data["title"] == "Ficção"
    assert data["slug"] == "ficcao"
    assert data["description"] == "Livros de ficção"
    assert data["active"] is True
