import PySimpleGUI as sg

from app.interface.elements import (
    TITLE_BAR,
    TOP_NAME,
    FOOTER_IMAGE,
    get_shop_frames,
    get_window
)
from app.events.utils import add_file
from app.events.update_prices import process_products_prices
from app.events.delete_products import process_product_delete


SHOPS = {
    'Тестовый магазин': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQxMDE2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc0NzQzNDk4NCwiaWQiOiIwMTkzMmY2NS0zZWFjLTdjYTktYjBkMC01ZmI1ZGFiOGRkYjEiLCJpaWQiOjEwMTc1NTI2OSwib2lkIjoxMTg2NjYzLCJzIjozODM4LCJzaWQiOiI5NmNlMGE2Yy0zYTNkLTQyYTItOWNhYS03YWVkOTBiMjVmY2YiLCJ0IjpmYWxzZSwidWlkIjoxMDE3NTUyNjl9._8EnoZLOqrdZA1R_EVAbcEKG_dTwTIYj61U7xqJXoBTxYhh4bHQLQXM-fu2na7y2f4UKLxVjpRDnU4nKL2I65g',
}

for shop in SHOPS:
    SHOPS[shop] = SHOPS[shop].strip()

main_layout = [
    [TITLE_BAR],
    [TOP_NAME],
]

main_layout += get_shop_frames(SHOPS)

main_layout += [FOOTER_IMAGE]

file_path = {}

window = get_window(main_layout)


def main() -> None:
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,):
            break
        if 'ADD_FILE' in event:
            add_file(event, values, file_path, window)
        if 'REFRESH' in event:
            process_products_prices(event, file_path, SHOPS, window)
        if 'DELETE_POPUP' in event:
            res = sg.PopupYesNo(
                (
                    'Вы уверены, что хотите перенести в корзину\n'
                    'товары из таблицы?'
                ),
            )

            if res == 'Yes':
                process_product_delete(event, file_path, SHOPS, window)

    window.close()


if __name__ == '__main__':
    main()
