import requests

from app.constants import WAREHOUSES_API_URL


def get_shop_warehouses(api_key: str) -> list[dict[str, str]] | None:

    headers = {"Authorization": api_key}

    try:
        response = requests.get(WAREHOUSES_API_URL, headers=headers)
        return response.json() if response.status_code == 200 else None
    except Exception:
        return None
