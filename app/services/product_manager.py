import time
from itertools import batched

from app.wb_api import (
    delete_product_stock,
    change_product_stock,
    get_shop_warehouses
)
from app.excel_processor import get_skus_and_amount
from app.services import InvalidAmountError
from app.constants import (
    UPDATE_AND_DELETE_REST_REQUEST_LIMIT,
    UPDATE_AND_DELETE_REST_REQUEST_WINDOW_SECONDS
)


def change_product_rest(
    api_key: str,
    excel_path: str
) -> tuple[bool, str | None]:

    warehouses = get_shop_warehouses(api_key)
    if not warehouses:
        return False, "Ошибка при получении складов."

    warehouse_ids = [w.get('id') for w in warehouses]

    stocks_to_remove, stocks = [], []
    try:
        for sku, amount in get_skus_and_amount(excel_path):
            if amount != 0:
                stocks.append(
                    {
                        "sku": sku,
                        "amount": amount,
                    }
                )
            else:
                stocks_to_remove.append(sku)

    except InvalidAmountError as e:
        return False, (
            "Ошибка: Неправильно передано количество\n"
            f"Товар - {e.sku}, Количество - {e.amount}"
        )

    if not stocks and not stocks_to_remove:
            return False, "Ошибка. Пустой список"

    errors = []

    request_counter = 0
    start_time = time.time()
    for warehouse_id in warehouse_ids:

        if not warehouse_id:
            continue

        for batch in batched(stocks, 1000):
            if request_counter >= UPDATE_AND_DELETE_REST_REQUEST_LIMIT:
                elapsed = time.time() - start_time
                if elapsed < UPDATE_AND_DELETE_REST_REQUEST_WINDOW_SECONDS:
                    time.sleep(
                        UPDATE_AND_DELETE_REST_REQUEST_WINDOW_SECONDS-elapsed
                    )
                request_counter = 0
                start_time = time.time()

            success, error = change_product_stock(
                api_key,
                warehouse_id,
                batch
            )
            request_counter += 1

            if not success:
                errors.append('Ошибка изменения остатка. '
                              f'Склад {warehouse_id}. {error}')

        for batch in batched(stocks_to_remove, 1000):
            if request_counter >= UPDATE_AND_DELETE_REST_REQUEST_LIMIT:
                elapsed = time.time() - start_time
                if elapsed < UPDATE_AND_DELETE_REST_REQUEST_WINDOW_SECONDS:
                    time.sleep(
                        UPDATE_AND_DELETE_REST_REQUEST_WINDOW_SECONDS-elapsed
                    )
                request_counter = 0
                start_time = time.time()

            success, error = delete_product_stock(
                api_key,
                warehouse_id,
                batch
            )
            request_counter += 1

            if not success:
                errors.append('Ошибка удаления остатка. '
                              f'Склад {warehouse_id}. {error}')

    return bool(errors), '\n\n'.join(errors) if errors else None
