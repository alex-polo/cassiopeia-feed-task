import logging
import pathlib
from datetime import datetime
from zoneinfo import ZoneInfo

from src.feed import build_yml
from src.feed.data import CATEGORIES, PRODUCTS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

log = logging.getLogger(__name__)


def main() -> None:
    """Main function."""
    result: str = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0, tzinfo=ZoneInfo("Europe/Moscow")),
    )

    print(result)  # noqa: T201

    output_path = "yml_catalog.xml"

    with pathlib.Path(output_path).open("w", encoding="utf-8") as f:
        f.write(result)

    log.info("Файл сохранён: %s", output_path)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.exception(e)
