import PySimpleGUI as sg

from interface.elements import get_window
from interface.layouts import main_layout


window = get_window(main_layout)


def main() -> None:
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == '__main__':
    main()
