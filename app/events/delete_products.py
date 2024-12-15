import requests
from openpyxl import load_workbook

from app.events.utils import get_shop_warehouses, get_product_card


def remove_product_rest(
    api_key: str,
    excel_path: str,
):

    TRASH_URL = (
        'https://content-api.wildberries.ru/content/v2/cards/delete/trash'
    )

    headers = {"Authorization": api_key}

    warehouses_data = get_shop_warehouses(api_key)
    warehouses_id = [*map(lambda x: x['id'], warehouses_data)]

    wb = load_workbook(excel_path)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2, max_col=0, values_only=True):

        article = row[0]
        product_data = get_product_card(api_key, article)
        skuses = [*map(lambda x: x['skus'], product_data['cards'][0]['sizes'])]
        nmID = product_data["cards"][0]["nmID"]

        for skus in skuses:

            params = {
                'skus': skus,
            }

            for id in warehouses_id:

                STOCKS_URL = (
                    'https://marketplace-api.wildberries.ru/'
                    f'api/v3/stocks/{id}'
                )

                requests.delete(
                    STOCKS_URL,
                    headers=headers,
                    json=params,
                )

        requests.post(
            TRASH_URL,
            headers=headers,
            json={'nmIDs': [nmID]}
        )


def process_product_delete(event, file_path, shops: dict, window):
    shop_name = event.removeprefix('DELETE_POPUP')

    api_key = shops[shop_name]

    path = file_path[shop_name]

    del file_path[shop_name]

    remove_product_rest(api_key, path)
