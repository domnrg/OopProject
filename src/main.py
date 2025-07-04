from typing import Optional, Dict, List


class Product:
    """Класс для создания продуктов"""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {int(self.price)} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        if not isinstance(other, Product):
            return NotImplemented
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов.")
        return self.price * self.quantity + other.price * other.quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif new_price < self.__price:
            answer = input("Цена снижается. Подтвердите понижение (y/n)").strip().lower()
            if answer == "y":
                self.__price = new_price
                print("Цена снижена")
            else:
                print("Действие отменено. Цена осталась прежней")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, data: dict) -> "Product":
        """Создаёт новый товар из словаря данных"""
        name = str(data.get("name", ""))
        description = str(data.get("description", ""))
        price = float(data.get("price", 0.0))
        quantity = int(data.get("quantity", 0))
        return cls(name, description, price, quantity)

    @staticmethod
    def merge_products(new_data: Dict, existing_products: List["Product"]) -> "Product":
        """Проверяет наличие продукта с таким же именем и обновляет его, если найден. Иначе — создаёт новый."""
        name = str(new_data.get("name", ""))
        description = str(new_data.get("description", ""))
        price = float(new_data.get("price", 0.0))
        quantity = int(new_data.get("quantity", 0))

        for product in existing_products:
            if product.name == name:
                product.quantity += quantity
                product.price = max(product.price, price)
                return product

        return Product(name, description, price, quantity)


class Category:
    """Класс для создания категорий"""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: Optional[list[Product]] = None) -> None:
        self.name = name
        self.description = description
        self.__products = products if products else []
        Category.category_count += 1
        Category.product_count += len(products) if products else 0

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @property
    def products(self) -> list:
        return self.__products

    def add_product(self, product: Product) -> None:
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product или его подклассов")

    @property
    def product_list(self) -> list:
        return [f"{str(product)}" for product in self.__products]

class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: str,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        return f"{super().__str__()} ({self.model}, {self.memory} ГБ, {self.color}, {self.efficiency})"

class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        return f"{super().__str__()} (страна: {self.country}, прорастает за {self.germination_period} дней, цвет: {self.color})"


if __name__ == "__main__":  # pragma: no cover
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    # print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    # print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    # print(product3.price)
    print(product3.quantity)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(category1.category_count)
    print(category1.product_count)

    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4],
    )

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.product_count)

    cat = Category("Смартфоны", "Описание", [product1, product2])
    for line in cat.product_list:
        print(line)

    p1 = Product("Iphone 15", "512GB, Gray", 210000.0, 5)
    products = [p1]

    new_data = {"name": "Iphone 15", "description": "512GB, Gray", "price": 215000.0, "quantity": 3}

    updated_product = Product.merge_products(new_data, products)

    # Добавим в список, если нового не было
    if updated_product not in products:
        products.append(updated_product)

    # Вывод
    for p in products:
        print(f"{p.name}, {p.price} руб., Остаток: {p.quantity} шт.")

    product = Product("Телевизор", "4K QLED", 50000, 10)

    print(f"Исходная цена: {product.price}")  # 50000

    print("\nПопытка установить цену -1000:")
    product.price = -1000  # Ожидаем: сообщение об ошибке

    print("\nПопытка снизить цену до 40000:")
    product.price = 40000  # Ожидаем: вопрос "y/n"

    print("\nПопытка повысить цену до 60000:")
    product.price = 60000  # Ожидаем: цена меняется без подтверждения

    print(f"\nТекущая цена: {product.price}")

    print(str(product1))
    print(str(category1))

    p1 = Product("Телевизор", "4K QLED", 100_000, 2)
    p2 = Product("Ноутбук", "Intel Core i7", 80_000, 3)

    total = p1 + p2  # 100_000 * 2 + 80_000 * 3 = 440_000
    print(total)

    smartphone = Smartphone(
        name="iPhone 15 Pro",
        description="Флагман от Apple",
        price=200_000.0,
        quantity=10,
        efficiency="высокая",
        model="A310",
        memory=512,
        color="серый"
    )

    grass = LawnGrass(
        name="Газон универсальный",
        description="Для всех типов почвы",
        price=1200.0,
        quantity=25,
        country="Нидерланды",
        germination_period=14,
        color="зеленый"
    )

    print(smartphone)
    print(grass)

    p1 = Smartphone("iPhone", "desc", 100_000, 2, "Apple", "13 Pro", 256, "серый")
    p2 = Smartphone("Samsung", "desc", 90_000, 1, "Samsung", "S21", 128, "чёрный")
    p3 = LawnGrass("Газон", "desc", 1000, 10, "Россия", 14, "зелёный")

    print(p1 + p2)  # OK
    #print(p1 + p3)

