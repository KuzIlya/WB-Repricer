from typing import TypeAlias, Any

import requests

from app.constants import GET_PRODUCT_CARD_API_URL


Payload: TypeAlias = dict[Any, Any]


def get_product_card(
    api_key: str,
    article: str,
) -> dict[Any, Any] | None:

    headers = {"Authorization": api_key}
    payload: Payload = {
        "settings": {                      
            "cursor": {
                "limit": 1
            },
            "filter": {
                "textSearch": f"{article}",
                "withPhoto": -1
            }
        }
    }

    try:
        response = requests.post(GET_PRODUCT_CARD_API_URL, headers=headers, json=payload)
        return response.json() if response.status_code == 200 else None
    except Exception:
        return None
