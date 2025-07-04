from unittest.mock import patch

import pytest

from src.main import Category, Product


def test_product_init(first_product: Product) -> None:
    assert first_product.name == "Samsung Galaxy S23 Ultra"
    assert first_product.description == "256GB, Серый цвет, 200MP камера"
    assert first_product.price == 180000.0
    assert first_product.quantity == 5


def test_category_init(first_category: Category) -> None:
    assert first_category.name == "Смартфоны"
    assert (
        first_category.description
        == "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )
    assert len(first_category.products) == 3


def test_category_and_product_counts(first_product: Product, second_product: Product, third_product: Product) -> None:
    # На момент начала теста счётчики должны быть сброшены
    assert Category.category_count == 0
    assert Category.product_count == 0

    # Создаём первую категорию с 3 продуктами
    _ = Category("Смартфоны", "Описание", [first_product, second_product, third_product])
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


def test_add_product(first_product: Product, second_product: Product, third_product: Product) -> None:
    cat = Category("Смартфоны", "Описание", [first_product, second_product, third_product])
    assert Category.category_count == 1
    assert Category.product_count == 3

    prod4 = Product("Test TV", "4K", 100000.0, 2)
    assert Category.product_count == 3

    cat.add_product(prod4)
    # Теперь product_count должен стать 4
    assert Category.product_count == 4

    # Проверим, что продукт действительно добавлен в список
    assert prod4 in cat.products
    assert len(cat.products) == 4


def test_product_list(first_product: Product, second_product: Product) -> None:
    category = Category("Тестовая категория", "Описание", [first_product, second_product])
    expected = [
        "Samsung Galaxy S23 Ultra, 180000 руб. Остаток: 5 шт.",
        "Iphone 15, 210000 руб. Остаток: 8 шт.",
    ]
    assert category.product_list == expected


def test_new_product() -> None:
    products = []  # пустой список
    new_data = {
        "name": "New Product",
        "description": "Описание",
        "price": 5000.0,
        "quantity": 2,
    }

    result = Product.merge_products(new_data, products)

    assert isinstance(result, Product)
    assert result.name == "New Product"
    assert result.price == 5000.0
    assert result.quantity == 2
    assert len(products) == 0


def test_merge_products(first_product: Product) -> None:
    products = [first_product]
    new_data = {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 185000.0,  # выше чем было
        "quantity": 3,
    }
    result = Product.merge_products(new_data, products)

    assert result is first_product  # обновился существующий товар
    assert result.price == 185000.0  # цена обновилась
    assert result.quantity == 8  # количество увеличилось


def test_product_price_getter_setter(first_product: Product) -> None:
    assert first_product.price == 180000.0
    first_product.price = 190000.0
    assert first_product.price == 190000.0


@patch("builtins.input", return_value="y")
def test_product_price_decrease_confirm(mock_input: object, first_product: Product) -> None:
    first_product.price = 150000.0
    assert first_product.price == 150000.0


@patch("builtins.input", return_value="n")
def test_product_price_decrease_cancel(mock_input: object, first_product: Product) -> None:
    original_price = first_product.price
    first_product.price = 100000.0
    assert first_product.price == original_price


def test_product_price_invalid(first_product: Product, capsys: pytest.CaptureFixture[str]) -> None:
    first_product.price = -500
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_product_str(first_product: Product):
    expected = "Samsung Galaxy S23 Ultra, 180000 руб. Остаток: 5 шт."
    assert str(first_product) == expected


def test_category_str(first_category: Category):
    expected = "Смартфоны, количество продуктов: 27 шт."
    assert str(first_category) == expected


def test_product_add(first_product: Product, second_product: Product) -> None:
    expected_total = first_product.price * first_product.quantity + second_product.price * second_product.quantity
    assert first_product + second_product == expected_total
