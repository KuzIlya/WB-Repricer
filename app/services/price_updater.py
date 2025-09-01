import time
from itertools import batched

from app.wb_api import upload_prices_batch
from app.excel_processor import get_articles_and_prices
from app.constants import UPDATE_ENDPOINT_TIME_RESTRICTION


def update_prices(
    api_key: str,
    excel_path: str,
) -> tuple[int, int] | None:

    goods = [
        {
            "nmID": article,
            "price": price,
        }
        for article, price in get_articles_and_prices(excel_path)
    ]

    if not goods:
        return None

    success, fail = 0, 0
    request_counter = 0
    start_time = time.time()
    
    for batch in batched(goods, 1000):
        if request_counter >= 10:
            elapsed = time.time() - start_time
            if elapsed < UPDATE_ENDPOINT_TIME_RESTRICTION:
                time.sleep(UPDATE_ENDPOINT_TIME_RESTRICTION - elapsed)
            request_counter = 0
            start_time = time.time()
        
        response = upload_prices_batch(api_key, list(batch))
        request_counter += 1
        
        if response and not response.get("error", True):
            success += len(batch)
        else:
            fail += len(batch)

    return success, fail
