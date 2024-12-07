import PySimpleGUI as sg

from shops_info import SHOPS

from .colors import (
    BLUE_COLOR,
    WHITE_COLOR,
    BLACK_COLOR,
    BUTTON_COLOR,
    LIGHT_BLUE_COLOR
)

MARKINES_IMAGE_BASE64 = b'iVBORw0KGgoAAAANSUhEUgAAAHUAAAAOCAYAAAAR4VO+AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAASKSURBVHgB7VhLbttIEH2UgpnNLDQncM8JLCfAALOycgJ7doOxB6ZvYJ9A9AmcOYEYJAiyC30C0asAARzJJzB9gjhAFgGCiKliN81is5siEyfZ+AEFsZvV39f1qingHj8Vr/+BWuxihDtEQDYR5bRDG2WMsSS7afGddOybFzVGN2TG2sZy+fjGKNegUK3rxtTLfmWdC7J/p++bfzEeDsnnM8bBANtmvJFsk+vfy88rJH++KPoYC59OYFJzUT4me9LizwPMxSCP4SdrShaJcptvSDZDd0RkJ1adXMchWSzKu2SnqEhj8IYdizmx/4F5PkdFZr5m3BIhqjXctr/YxzTQ4yv0ICcPcPzoWcFFRraBHhhYZV74gcdXkb3qODH2jay6GXBnMhOhHplt8+BD+Ar1KGQyt9BNmexxr1A/HF4QoVEQIMyZ5KBF0fhdjjMmkg7A4+ABfjeEfhUeOOpi8/tU1CnozVHohrmjTkFH77HjXQodyesQozq1E7STcmTGkwfpf2hi2lLGOiiyBfQ64jbHIMeYCD179LyYy9GC5Hc1QEj1xZxIglN8Qrr1sp4qOM+SVCsjvxI85tIzp7AsuEhl8Cm5NB1wgz6EMv4QzxNUJPPiztAkgzc5w92BFUeSyXIYoX9k+sB9s/JwXmQ5zlxOeY6EInX2dh+b+QpPP66Q/vWi2IMailwb0D4F2A70fo04atEkcBN+tUvLB5vUBFr/uSETwblJ5iKOXp88A9aJEchEH7wZLH0yWnbRL6eWffogF56imwp0AffD81SmHEKT8LfTe1iQkJG0XgdDTH8dFASnRDYfbBDhO6guQpcU1WnAZA6RPIydahKiI3JhE+gozR228PhLzD1tbTt1TDbvYa580+Z/hfW361j4p55+FTQBrj1a2O3f7iGhvHo718U+JkRqTLZkcvkd1y3CevQZ+S3nm6Hf3uQu+T0yEz8QddzxutMeon79v3T4bIsxXDJc4tCMyeSPrXkcYr2Mnph2O6asoDc9RotcdgSvjefP0jhFFbWNQ5NTzqT8eUrkbWBF6/1AEZg0o40JvNgr9m6TIrVQSiG/pXIC/k9IbjsvC76cypPeNBPNoAltu1wo6AWW8F0i5qiIn6EpwyVSMy6/j0TfyrQ7QfslJTPtQtQ3PjTjx/B/mnRFbOY5g/8mvkF5MiNi35OkTvPfMCOCE4qn8+KtyKFk1xRmSSG/dHl6WF2eElSXQx+pjTzrk9ORmbTq4B+LurbcOLbaR6Y+RFPmJPj9O8tnZvnJd6GoZx+XXF5BRwEca0g9/Sq4EVl+RXsjv1HpZMnv0sjvri2//A8TS7ApZvgK+T0X/d1YzxM0ce7wUaK+LQLKD/5yM7ntyPTjmwcjht6oWNTxDTsyllntM+uZlecJmtFdpprY6kPeOtvmVSIyfcSy/a387mGD5PRs63kRdandmAm8+I/2hP9pGmKHLlLqF72PkekrQw8EuMd3BUdizoeYb7or3PANlwkmshU4hw7oYOvna/pN6SAsB5+Q2N+ufXBP6g9EjWDKs5xDBwFFouMPiG/BF7A71mLQL22LAAAAAElFTkSuQmCC'

TITLE_BAR = sg.Titlebar(
    'Markines Repricer',
    text_color=BLACK_COLOR,
    background_color=BLUE_COLOR,
    icon=None,
)


TOP_NAME = sg.Text(
    'REPRICER',
    font=('Anonymous Pro', 25),
    expand_x=True,
    justification='c',
    background_color=WHITE_COLOR,
    text_color=BLACK_COLOR
)


FOOTER_IMAGE = [
    sg.Column(
        [
            [
                sg.Image(
                    data=MARKINES_IMAGE_BASE64,
                    background_color=WHITE_COLOR,
                )
            ]
        ],
        justification='center',
    )
]


def get_window(
    layout: list[list[sg.Element]]
) -> sg.Window:
    return sg.Window(
        'Window Title',
        layout,
        size=(800, 500),
        background_color=WHITE_COLOR
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
            sg.Button(
                'Загрузить',
                button_color=BUTTON_COLOR,
                mouseover_colors=LIGHT_BLUE_COLOR,
                border_width=0,
            ),
            sg.Button(
                'Обновить',
                button_color=BUTTON_COLOR,
                mouseover_colors=LIGHT_BLUE_COLOR,
                border_width=0,
            ),
        ]
    ]

    return sg.Frame(
        '',
        additional_layout,
        border_width=0,
        background_color=BLUE_COLOR,
        expand_x=True,
        relief=sg.RELIEF_FLAT
    )


def get_shop_frames() -> list[sg.Frame]:
    result_layout = []
    for shop in SHOPS:
        result_layout.append([get_shop_frame(shop)])
    return result_layout
