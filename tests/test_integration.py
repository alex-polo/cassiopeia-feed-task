import xml.etree.ElementTree as ET  # noqa: S405
from datetime import datetime


class TestBuildYmlFullIntegration:
    """Full integration test."""

    def _get_int_attr(self, element: ET.Element, attr: str) -> int:
        """Get integer attribute."""
        value: str | None = element.get(attr)
        assert value is not None, f"Missing attribute: {attr}"
        return int(value)

    def _get_element(self, parent: ET.Element, path: str) -> ET.Element:
        """Find element by path. Asserts it exists."""
        element = parent.find(path)
        assert element is not None, f"Element not found: {path}"
        return element

    def _get_text(self, parent: ET.Element, path: str) -> str:
        """Find element and return its text. Asserts both exist."""
        element = self._get_element(parent, path)
        assert element.text is not None, f"Element has no text: {path}"
        return element.text

    def _element_not_exists(self, parent: ET.Element, path: str) -> None:
        """Assert element does not exist."""
        assert parent.find(path) is None, f"Element should not exist: {path}"

    def test_date_format(
        self,
        yml_document: ET.Element,
        time_generated_at: datetime,
    ) -> None:
        """Test date."""
        assert yml_document.get("date") == time_generated_at.strftime("%Y-%m-%d %H:%M")

    def test_categories_unique_and_sorted(self, yml_document: ET.Element) -> None:
        """Test categories."""
        category_ids = [
            self._get_int_attr(element=category, attr="id")
            for category in yml_document.findall(".//categories/category")
        ]

        assert category_ids == [1, 2]

    def test_offers_ids(self, yml_document: ET.Element) -> None:
        """Test offers."""
        offer_ids = [
            self._get_int_attr(element=offer, attr="id")
            for offer in yml_document.findall(".//offer")
        ]

        assert offer_ids == [101, 102, 107]

    def test_product_fields(self, yml_document: ET.Element) -> None:
        """Test offers."""
        # Товар 101: все поля должны присутствовать
        offer_101 = self._get_element(yml_document, ".//offer[@id='101']")
        assert offer_101.get("available") == "true"
        assert self._get_text(offer_101, "price") == "490.00"
        assert self._get_text(offer_101, "oldprice") == "590.00"
        assert self._get_text(offer_101, "name") == 'Чай "Лес & травы" <сбор №1>'
        assert (
            self._get_text(offer_101, "description")
            == "Вкус: мята & чабрец > классический чай"
        )

        # Товар 102: Если old_price меньше price, то должен отсутствовать,  # noqa: W505
        # Если stock=0 то available=false
        offer_102 = self._get_element(yml_document, ".//offer[@id='102']")
        assert offer_102.get("available") == "false"
        assert self._get_text(offer_102, "price") == "1500.00"
        self._element_not_exists(offer_102, "oldprice")

        # Товар 107: нет old_price и description
        offer_107 = self._get_element(yml_document, ".//offer[@id='107']")
        assert offer_107.get("available") == "true"
        assert self._get_text(offer_107, "price") == "700.50"
        self._element_not_exists(offer_107, "oldprice")
        self._element_not_exists(offer_107, "description")
