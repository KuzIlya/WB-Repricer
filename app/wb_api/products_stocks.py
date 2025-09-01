import requests

from app.constants import PRODUCT_STOCKS_API_URL


def delete_product_stock(
    api_key: str,
    warehouse_id: str,
    skus: list[str],
) -> bool:

    url = PRODUCT_STOCKS_API_URL.format(warehouse_id)
    headers = {"Authorization": api_key}
    payload = {'skus': skus}
    
    try:
        response = requests.delete(url, headers=headers, json=payload)
        return response.status_code in (204, 404)
    except Exception:
        return False
