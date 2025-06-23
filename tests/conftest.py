import pytest

from src.main import Category, Product


@pytest.fixture
def first_product() -> Product:
    return Product(
        name="Samsung Galaxy S23 Ultra",
        description="256GB, Серый цвет, 200MP камера",
        price=180000.0,
        quantity=5,
    )


@pytest.fixture
def second_product() -> Product:
    return Product(name="Iphone 15", description="512GB, Gray space", price=210000.0, quantity=8)


@pytest.fixture
def third_product() -> Product:
    return Product(
        name="Xiaomi Redmi Note 11",
        description="1024GB, Синий",
        price=31000.0,
        quantity=14,
    )


@pytest.fixture
def first_category(first_product: Product, second_product: Product, third_product: Product) -> Category:
    return Category(
        name="Смартфоны",
        description="Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        products=[first_product, second_product, third_product],
    )


@pytest.fixture(autouse=True)
def reset_category_counts() -> None:
    """Сброс глобальных счётчиков категорий и продуктов перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
