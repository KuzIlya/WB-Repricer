from typing import Any

import requests

from app.constants import PRODUCT_STOCKS_API_URL


def change_product_stock(
    api_key: str,
    warehouse_id: str,
    stock: list[dict[str, Any]],
) -> tuple[bool, str | None]:

    url = PRODUCT_STOCKS_API_URL.format(warehouse_id)
    headers = {'Authorization': api_key}
    payload = {'stocks': stock}

    try:
        response = requests.put(url, headers=headers, json=payload)
        match response.status_code:
            case 204:
                return True, None
            case 406:
                return (
                    False,
                    f'Статус ошибки {response.status_code}. '
                    'Обновление остатков заблокировано'
                )
            case 409:
                base_line = (f'Статус ошибки {response.status_code}. '
                             'Товар не найден.\n'
                             'Не найденные товары:\n')
                base_line += '\n'.join(
                    [sku['sku'] for sku in response.json()[0]['data']]
                )
                return (
                    False,
                    base_line
                )
            case 429:
                return (
                    False,
                    f'Статус ошибки {response.status_code}. '
                    'Слишком много запросов'
                )
            case _:
                return (
                    False,
                    f'Ошибка {response.status_code}: {response.text}'
                )

    except Exception as e:
        return False, f'Ошибка {e}'


def delete_product_stock(
    api_key: str,
    warehouse_id: str,
    skus: list[str],
) -> tuple[bool, str | None]:

    url = PRODUCT_STOCKS_API_URL.format(warehouse_id)
    headers = {"Authorization": api_key}
    payload = {'skus': skus}
    
    try:
        response = requests.delete(url, headers=headers, json=payload)
        match response.status_code:
            case 204:
                return True, None
            case 404:
                base_line = (f'Статус ошибки {response.status_code}. '
                             'Товар не найден на складе.\n'
                             'Не найденные товары:\n')
                base_line += '\n'.join(response.json()['data'])
                return (
                        False,
                        base_line
                    )
            case 409:
                return (
                    False,
                    f'Статус ошибки {response.status_code}. '
                    'Склад находится в процессе обновления или удаления. '
                    'Повторите попытку через несколько секунд.'
                )
            case 429:
                return (
                    False,
                    f'Статус ошибки {response.status_code}. '
                    'Слишком много запросов'
                )
            case _:
                return (
                    False,
                    f'Ошибка {response.status_code}: {response.text}'
                )

    except Exception as e:
        return False, f'Ошибка {e}'
