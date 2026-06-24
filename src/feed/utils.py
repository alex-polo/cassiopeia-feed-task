from decimal import Decimal, InvalidOperation
from typing import Any


def is_valid_product(
    product: dict[str, Any],
    categories_map: dict[int, dict[str, Any]],
) -> bool:
    """3. Правила включения товаров.

    В фид включаются только товары,
    которые одновременно соответствуют следующим условиям:
    ·	товар активен;
    ·	категория товара активна;
    ·	название товара не пустое;
    ·	цена товара больше нуля;
    ·	указана ссылка на изображение;
    ·	ссылка на изображение начинается с http:// или https://.

    Согласно предоставленным исходным данным,
    в фид должны попасть только товары: 101, 102 и 107
    Товары 103, 104, 105 и 106 в фиде присутствовать не должны.
    """
    # 1. товар активен
    if not product.get("is_active"):
        return False

    # 2. категория товара активна
    product_category_id = product.get("category_id")
    if product_category_id is None:
        return False

    category = categories_map.get(product_category_id)

    if not category or not category.get("is_active"):
        return False

    # 3. название не пустое
    if not product.get("name"):
        return False

    # 4. цена больше нуля
    if parse_price(product.get("price")) is None:
        return False

    # 5. указана ссылка на изображение
    # 6. ссылка на изображение начинается с http:// или https://.
    image_url = product.get("image_url")

    return bool(image_url and image_url.startswith(("http://", "https://")))


def parse_price(price: str | None) -> Decimal | None:
    """7. Цена.

    Цена должна:
    ·	быть больше нуля;
    ·	выводиться с точкой в качестве десятичного разделителя;
    ·	содержать два знака после точки.

    Ожидаемые значения:
        <price>490.00</price>
        <price>1500.00</price>
        <price>700.50</price>
    """
    if price is None:
        return None

    try:
        price_decimal = Decimal(price)
        if price_decimal <= 0:
            return None

        return price_decimal
    except (InvalidOperation, ValueError, TypeError):
        return None


def format_availability(stock: int) -> str:
    """6. Наличие товара.

    Атрибут available должен иметь только строковое
    значение true или false.

    Правило:
    ·	true, если stock > 0;
    ·	false, если stock == 0.

    Ожидаемый результат:
        <offer id="101" available="true">
        <offer id="102" available="false">
        <offer id="107" available="true">

    Яндекс использует значения true и false для передачи
    возможности купить товар.
    """
    return "true" if stock > 0 else "false"


def parse_old_price(price: Decimal | None, old_price: str | None) -> Decimal | None:
    """8. Old Price.

    Элемент <oldprice> необходимо добавлять только в том
    случае, если старая цена:
    ·	указана;
    ·	больше нуля;
    ·	строго больше текущей цены.

    Поэтому:
    ·	у товара 101 элемент <oldprice> должен присутствовать;
    ·	у товара 102 элемент <oldprice> должен отсутствовать,
        поскольку 1400.00 меньше текущей цены 1500.00;
    ·	у товара 107 элемент должен отсутствовать.

    Ожидаемое значение для товара 101:
    <oldprice>590.00</oldprice>

    Официальные требования также предусматривают,
    что старая цена должна быть выше текущей.
    """
    if old_price is None or price is None:
        return None

    parsed_old_price = parse_price(old_price)
    if parsed_old_price is not None and parsed_old_price > price:
        return parsed_old_price

    return None


def format_product(product: dict[str, Any], base_url: str) -> dict[str, Any]:
    """Форматируем продукт."""
    # парсим цены
    price: Decimal | None = parse_price(product.get("price"))
    old_price: Decimal | None = parse_old_price(
        price=price, old_price=product.get("old_price")
    )
    # форматируем цены
    formatted_price: str | None = f"{price:.2f}" if price is not None else None
    formatted_old_price: str | None = (
        f"{old_price:.2f}" if old_price is not None else None
    )
    # доступность товара
    formatted_available: str = format_availability(product.get("stock", 0))
    # описание товара
    description: str | None = product.get("description") or None
    # картинка товара
    image_url: str | None = product.get("image_url")

    return {
        "id": product["id"],
        "url": f"{base_url}/products/{product['slug']}/",
        "price": formatted_price,
        "old_price": formatted_old_price,
        "currency_id": "RUB",
        "category_id": product["category_id"],
        "picture": image_url,
        "name": product["name"],
        "description": description,
        "available": formatted_available,
    }
