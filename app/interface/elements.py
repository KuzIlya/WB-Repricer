import PySimpleGUI as sg

from .colors import (
    BLUE_COLOR,
    WHITE_COLOR,
    BLACK_COLOR,
    BUTTON_COLOR,
    LIGHT_BLUE_COLOR
)

from .images_base64 import MARKINES_IMAGE_BASE64

TITLE_BAR = sg.Titlebar(
    'Markines Repricer',
    text_color=BLACK_COLOR,
    background_color=BLUE_COLOR,
    icon=None,
)


TOP_NAME = sg.Text(
    'REPRICER',
    font=('Anonymous Pro', 25, 'bold'),
    expand_x=True,
    justification='c',
    background_color=WHITE_COLOR,
    text_color=BLACK_COLOR
)


FOOTER_IMAGE = [
    sg.Frame(
        '',
        [
            [
                sg.Image(
                    data=MARKINES_IMAGE_BASE64,
                    background_color=WHITE_COLOR,
                    expand_y=True,
                    pad=((330, 0), (0, 0))
                )
            ]
        ],
        vertical_alignment='b',
        background_color=WHITE_COLOR,
        border_width=0
    )
]


def get_window(
    layout: list[list[sg.Element]]
) -> sg.Window:
    return sg.Window(
        'Window Title',
        layout,
        size=(800, 500),
        background_color=WHITE_COLOR,
    )


def get_shop_frame(name: str) -> sg.Frame:

    additional_layout = [
        [
            sg.Text(
                name,
                background_color=BLUE_COLOR,
                justification='l',
                expand_x=True
            ),
            sg.FileBrowse(
                'Загрузить',
                enable_events=True,
                button_color=BUTTON_COLOR,
                file_types=[
                    ('xlsx files', '*.xlsx')
                ],
                target=('ADD_FILE' + name),
                key=('ADD_FILE' + name)
            ),
            sg.Button(
                'Удалить товары',
                button_color=BUTTON_COLOR,
                mouseover_colors=LIGHT_BLUE_COLOR,
                border_width=0,
                disabled=True,
                target=('DELETE_POPUP' + name),
                key=('DELETE_POPUP' + name),
            ),
            sg.Button(
                'Обновить цены',
                button_color=BUTTON_COLOR,
                mouseover_colors=LIGHT_BLUE_COLOR,
                border_width=0,
                disabled=True,
                target=('REFRESH' + name),
                key=('REFRESH' + name),
            ),
        ]
    ]

    return sg.Frame(
        '',
        additional_layout,
        border_width=0,
        background_color=BLUE_COLOR,
        expand_x=True,
        pad=((45, 45), (2, 2)),
        relief=sg.RELIEF_FLAT
    )


def get_shop_frames(shops: dict) -> list[sg.Frame]:
    result_layout = []
    for shop in shops:
        result_layout.append([get_shop_frame(shop)])
    return result_layout
