from decimal import Decimal
from typing import Any

import pytest

from src.feed.utils import (
    format_availability,
    format_product,
    is_valid_product,
    parse_old_price,
    parse_price,
)


class TestParsePrice:
    """Test parse_price function."""

    def test_valid_price(self) -> None:
        """Test valid price."""
        assert parse_price("490.00") == Decimal("490.00")

    def test_zero_price_returns_none(self) -> None:
        """Test zero price."""
        assert parse_price("0.00") is None

    def test_invalid_string_returns_none(self) -> None:
        """Test invalid string."""
        assert parse_price("str_value") is None

    def test_none_returns_none(self) -> None:
        """Test None."""
        assert parse_price(None) is None


class TestParseOldPrice:
    """Test parse_old_price function."""

    def test_higher_than_current(self) -> None:
        """Test higher than current."""
        assert parse_old_price(
            price=Decimal("490.00"),
            old_price="590.00",
        ) == Decimal("590.00")

    def test_lower_than_current_returns_none(self) -> None:
        """Test lower than current."""
        assert (
            parse_old_price(
                price=Decimal("1500.00"),
                old_price="1400.00",
            )
            is None
        )

    def test_none_returns_none(self) -> None:
        """Test None."""
        assert parse_old_price(price=Decimal("490.00"), old_price=None) is None


class TestFormatAvailability:
    """Test format_availability function."""

    def test_positive_stock(self) -> None:
        """Test positive stock."""
        assert format_availability(12) == "true"

    def test_zero_stock(self) -> None:
        """Test zero stock."""
        assert format_availability(0) == "false"

    def test_negative_stock(self) -> None:
        """Test negative stock."""
        assert format_availability(-1) == "false"


class TestIsValidProduct:
    """Test is_valid_product function."""

    @pytest.mark.parametrize(
        "product_id,expected",
        [
            (101, True),
            (102, True),
            (103, False),
            (104, False),
            (105, False),
            (106, False),
            (107, True),
        ],
    )
    def test_product_filtering(
        self,
        product_id: int,
        expected: bool,
        products: list[dict[str, Any]],
        categories_map_by_id: dict[int, dict[str, Any]],
    ) -> None:
        """Test product filtering."""
        product = next(p for p in products if p["id"] == product_id)
        assert is_valid_product(product, categories_map_by_id) is expected

    def test_invalid_image_url(
        self,
        categories_map_by_id: dict[int, dict[str, Any]],
    ) -> None:
        """Test invalid image url."""
        product = {
            "id": 999,
            "name": "Test",
            "category_id": 1,
            "price": "100.00",
            "image_url": "fake-url",
            "is_active": True,
        }

        assert is_valid_product(product, categories_map_by_id) is False


class TestFormatProduct:
    """Test format_product function."""

    def test_format_product_101(
        self,
        products: list[dict[str, Any]],
        base_url: str,
    ) -> None:
        """Товар 101.

        Есть old_price, description, available=true.
        """
        product = next(p for p in products if p["id"] == 101)
        result = format_product(product, base_url)

        assert result["price"] == "490.00"
        assert result["old_price"] == "590.00"
        assert result["available"] == "true"
        assert result["description"] == "Вкус: мята & чабрец > классический чай"

    def test_format_product_102(
        self,
        products: list[dict[str, Any]],
        base_url: str,
    ) -> None:
        """Товар 102.

        old_price < price, поле должно отсутствовать,
        Если stock=0, available=false.
        """
        product = next(p for p in products if p["id"] == 102)
        result = format_product(product, base_url)

        assert result["old_price"] is None
        assert result["available"] == "false"

    def test_format_product_107(
        self,
        products: list[dict[str, Any]],
        base_url: str,
    ) -> None:
        """Товар 107.

        Нет old_price, пустой description .
        """
        product = next(p for p in products if p["id"] == 107)
        result = format_product(product, base_url)

        assert result["price"] == "700.50"
        assert result["old_price"] is None
        assert result["description"] is None
