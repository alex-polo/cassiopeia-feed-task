import xml.etree.ElementTree as ET  # noqa: S405
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from src.feed.constants import BASE_URL
from src.feed.data import CATEGORIES, PRODUCTS
from src.feed.feed_task import build_yml


@pytest.fixture()
def time_generated_at() -> datetime:
    """Returns a datetime object."""
    return datetime(2026, 6, 18, 12, 0, tzinfo=ZoneInfo("Europe/Moscow"))


@pytest.fixture
def categories() -> list[dict[str, Any]]:
    """Returns a list of categories."""
    return CATEGORIES


@pytest.fixture
def products() -> list[dict[str, Any]]:
    """Returns a list of products."""
    return PRODUCTS


@pytest.fixture
def base_url() -> str:
    """Returns the base URL."""
    return BASE_URL


@pytest.fixture
def categories_map_by_id(categories: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    """Returns a dict of categories by id."""
    return {cat["id"]: cat for cat in categories}


@pytest.fixture
def yml_document(
    products: list[dict[str, Any]],
    categories: list[dict[str, Any]],
    time_generated_at: datetime,
) -> ET.Element:
    """Returns a yml document."""
    yml_catalog = build_yml(
        products=products,
        categories=categories,
        generated_at=time_generated_at,
    )
    return ET.fromstring(yml_catalog)  # noqa: S314
