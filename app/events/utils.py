import requests
import time
from typing import Optional
import PySimpleGUI as sg


def add_file(
    event,
    values,
    file_path: dict,
    window: sg.Window
) -> None:
    shop_name = event.removeprefix('ADD_FILE')
    file_path[shop_name] = values[event]

    refresh_button = window.find_element('REFRESH' + shop_name)
    delete_popup_button = window.find_element('DELETE_POPUP' + shop_name)

    refresh_button.update(disabled=False)
    delete_popup_button.update(disabled=False)

    window.refresh()


def get_product_card(
    api_key: str,
    article: str,
    retries: int = 3
) -> Optional[dict]:
    """
    Получает данные карточки товара по артикулу.

    :param api_key: API-ключ для авторизации.
    :param article: Артикул товара.
    :param retries: Количество попыток при ошибках.
    :return: JSON с данными карточки товара или None в случае неудачи.
    """
    url = "https://content-api.wildberries.ru/content/v2/get/cards/list"
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    params = {
        "settings": {
            "cursor": {
                "limit": 100
            },
            "filter": {
                "withPhoto": 1,
                "textSearch": str(article)
            }
        }
    }

    for attempt in range(retries):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=params,
                timeout=60
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Попытка {attempt + 1}/{retries} завершилась ошибкой: {e}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise e
    return None


def get_shop_warehouses(
    api_key: str,
    retries: int = 3
) -> list[dict] | None:
    """
    Получает список складов магазина.

    :param api_key: API-ключ для авторизации.
    :param retries: Количество попыток при ошибках.
    :return: JSON с данными складов или None в случае неудачи.
    """
    url = "https://marketplace-api.wildberries.ru/api/v3/offices"
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }

    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=60
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Попытка {attempt + 1}/{retries} завершилась ошибкой: {e}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise e
    return None
