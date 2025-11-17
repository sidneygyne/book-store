import pytest
from product.models.product import Product
from product.models.category import Category
from product.serializers.product_serializer import ProductSerializer


@pytest.mark.django_db
def test_product_serializer_with_category():
    # Cria uma categoria
    category = Category.objects.create(
        title="Romance",
        slug="romance",
        description="Categoria de livros de romance",
        active=True
    )

    # Cria um produto e associa à categoria
    product = Product.objects.create(
        title="Livro A",
        description="Um livro de romance",
        price=50,
        active=True
    )
    product.categories.add(category)

    # Serializa o produto
    serializer = ProductSerializer(product)
    data = serializer.data

    # Valida os campos
    assert data["title"] == "Livro A"
    assert data["description"] == "Um livro de romance"
    assert data["price"] == 50
    assert data["active"] is True

    # Valida que a categoria