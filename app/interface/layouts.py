from interface.elements import (
    TITLE_BAR,
    TOP_NAME,
    FOOTER_IMAGE,
    get_shop_frames,
)


main_layout = [
    [TITLE_BAR],
    [TOP_NAME],
]

main_layout += get_shop_frames()

main_layout += [FOOTER_IMAGE]
