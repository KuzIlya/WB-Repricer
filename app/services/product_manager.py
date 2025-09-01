from itertools import batched

from app.wb_api import (
    delete_product_stock,
    get_shop_warehouses,
)
from app.excel_processor import get_skus


def remove_product_rest(
    api_key: str,
    excel_path: str
) -> tuple[bool, str | None]:

    warehouses = get_shop_warehouses(api_key)

    if not warehouses:
        return True, "Ошибка при получении складов."

    warehouse_ids = [w.get('id') for w in warehouses]
    errors = []

    for warehouse_id in warehouse_ids:

        if not warehouse_id:
            continue

        for batch in batched(get_skus(excel_path), 1000):
            if not delete_product_stock(api_key, warehouse_id, list(batch)):
                errors.append(f"SKU {batch}, склад {warehouse_id}: ошибка удаления остатка")

    return bool(errors), '\n'.join(errors) if errors else None
