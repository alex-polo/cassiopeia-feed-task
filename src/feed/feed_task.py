from datetime import datetime
from typing import Any

from .constants import BASE_URL, COMPANY, COMPANY_NAME
from .utils import format_product, is_valid_product
from .xml_builder import build_xml


def build_yml(
    products: list[dict[str, Any]],
    categories: list[dict[str, Any]],
    generated_at: datetime,
) -> str:
    """Builds YML catalog file."""
    # Создаём словарь категорий для быстрого поиска
    categories_map_by_id: dict[int, dict[str, Any]] = {
        category["id"]: category for category in categories
    }

    # Фильтрация продуктов по критериям ТЗ
    filtered_products: list[dict[str, Any]] = [
        product
        for product in products
        if is_valid_product(product, categories_map_by_id)
    ]

    # Собираем уникальные категории из отформатированных продуктов
    # сортируем в порядке возрастания
    unique_category_ids: set[int] = {
        product["category_id"] for product in filtered_products
    }
    filtered_categories: list[dict[str, Any]] = sorted(
        [categories_map_by_id[cat_id] for cat_id in unique_category_ids],
        key=lambda category: category["id"],
    )

    # форматирование полей продуктов (цена и тд)
    # сортируем в порядке возврастания
    formatted_products: list[dict[str, Any]] = sorted(
        [
            format_product(product=product, base_url=BASE_URL)
            for product in filtered_products
        ],
        key=lambda product: product["id"],
    )

    return build_xml(
        base_url=BASE_URL,
        company=COMPANY,
        company_name=COMPANY_NAME,
        generated_at=generated_at,
        filtered_categories=filtered_categories,
        formatted_products=formatted_products,
    )
