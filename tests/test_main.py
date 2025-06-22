from src.main import Category, Product


def test_product_init(first_product):
    assert first_product.name == "Samsung Galaxy S23 Ultra"
    assert first_product.description == "256GB, Серый цвет, 200MP камера"
    assert first_product.price == 180000.0
    assert first_product.quantity == 5


def test_category_init(first_category):
    assert first_category.name == "Смартфоны"
    assert (
        first_category.description
        == "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )
    assert len(first_category.products) == 3


def test_category_and_product_counts(first_product, second_product, third_product):

    # На момент начала теста счётчики должны быть сброшены
    assert Category.category_count == 0
    assert Category.product_count == 0

    # Создаём первую категорию с 3 продуктами
    _ = Category(
        "Смартфоны", "Описание", [first_product, second_product, third_product]
    )
    assert Category.category_count == 1
    assert Category.product_count == 3

    # Добавим ещё одну категорию с 1 продуктом
    prod4 = Product("Test TV", "4K", 100000.0, 2)
    _ = Category("Телевизоры", "Описание", [prod4])
    assert Category.category_count == 2
    assert Category.product_count == 4

    # Добавим ещё одну категорию без продуктов
    _ = Category("Пустая категория", "Нет товаров", [])
    assert Category.category_count == 3
    assert Category.product_count == 4  # не увеличился
