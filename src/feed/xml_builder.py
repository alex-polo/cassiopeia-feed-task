import xml.etree.ElementTree as ET  # noqa: S405
from datetime import datetime
from typing import Any


def create_root_xml_element(generated_at: datetime) -> ET.Element:
    """Creates the root XML element."""
    return ET.Element(
        "yml_catalog",
        attrib={"date": generated_at.strftime("%Y-%m-%d %H:%M")},
    )


def create_shop_xml_element(
    root_xml_element: ET.Element,
    base_url: str,
    company: str,
    company_name: str,
) -> ET.Element:
    """Creates the shop XML element."""
    shop_xml_element = ET.SubElement(root_xml_element, "shop")
    ET.SubElement(shop_xml_element, "name").text = company_name
    ET.SubElement(shop_xml_element, "company").text = company
    ET.SubElement(shop_xml_element, "url").text = base_url

    currencies_xml_element = ET.SubElement(shop_xml_element, "currencies")
    ET.SubElement(
        currencies_xml_element,
        "currency",
        attrib={"id": "RUB", "rate": "1"},
    )

    return shop_xml_element


def create_categories_xml_elements(
    shop_xml_element: ET.Element,
    categories: list[dict[str, Any]],
) -> None:
    """Creates the categories XML element."""
    categories_xml_element = ET.SubElement(shop_xml_element, "categories")
    for category in categories:
        ET.SubElement(
            categories_xml_element,
            "category",
            attrib={"id": str(category["id"])},
        ).text = category["name"]


def create_offers_xml_elements(
    shop_xml_element: ET.Element,
    formatted_products: list[dict[str, Any]],
) -> None:
    """Creates the offers XML element."""
    offers_xml_element = ET.SubElement(shop_xml_element, "offers")
    for product in formatted_products:
        offer_xml_element = ET.SubElement(
            offers_xml_element,
            "offer",
            attrib={
                "id": str(product["id"]),
                "available": product["available"],
            },
        )
        ET.SubElement(offer_xml_element, "url").text = product["url"]
        ET.SubElement(offer_xml_element, "price").text = product["price"]

        if product["old_price"] is not None:
            ET.SubElement(offer_xml_element, "oldprice").text = product["old_price"]

        ET.SubElement(offer_xml_element, "currencyId").text = product["currency_id"]
        ET.SubElement(offer_xml_element, "categoryId").text = str(
            product["category_id"]
        )
        ET.SubElement(offer_xml_element, "picture").text = product["picture"]
        ET.SubElement(offer_xml_element, "name").text = product["name"]

        if product["description"] is not None:
            ET.SubElement(offer_xml_element, "description").text = product[
                "description"
            ]


def build_xml(
    base_url: str,
    company: str,
    company_name: str,
    generated_at: datetime,
    filtered_categories: list[dict[str, Any]],
    formatted_products: list[dict[str, Any]],
) -> str:
    """Builds YML catalog file."""
    # Create the root XML element
    root_xml_element = create_root_xml_element(generated_at=generated_at)
    shop_xml_element = create_shop_xml_element(
        root_xml_element=root_xml_element,
        base_url=base_url,
        company=company,
        company_name=company_name,
    )

    # Create the categories XML element
    create_categories_xml_elements(
        shop_xml_element=shop_xml_element,
        categories=filtered_categories,
    )

    # Create the offers XML element
    create_offers_xml_elements(
        shop_xml_element=shop_xml_element,
        formatted_products=formatted_products,
    )
    # Indent the XML elements for better readability
    ET.indent(root_xml_element, space="  ")
    return ET.tostring(root_xml_element, encoding="unicode", xml_declaration=True)
