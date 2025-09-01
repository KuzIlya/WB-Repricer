from typing import Any

import requests

from app.constants import PRODUCT_PRICES_API_URL


def upload_prices_batch(
    api_key: str,
    batch: list[dict[str, Any]],
) -> dict[Any, Any] | None:

    headers = {"Authorization": api_key}
    payload = {"data": batch}
    
    try:
        response = requests.post(PRODUCT_PRICES_API_URL, headers=headers, json=payload)
        return response.json() if response.status_code == 200 else None
    except Exception:
        return None
