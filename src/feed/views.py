from datetime import datetime
from zoneinfo import ZoneInfo

from django.http import HttpRequest, HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET

from .data import CATEGORIES, PRODUCTS
from .feed_task import build_yml


@require_GET
@cache_page(timeout=60 * 5)
def yml_feed_view(request: HttpRequest) -> HttpResponse:
    """View for YML feed."""
    xml_content = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0, tzinfo=ZoneInfo("Europe/Moscow")),
    )

    return HttpResponse(
        xml_content,
        content_type="application/xml; charset=utf-8",
    )
