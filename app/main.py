import sys

from PyQt6.QtWidgets import QApplication
from loguru import logger

from app.ui.main_window import MainWindow
from app.config import SHOPS


def main() -> None:

    logger.info('Запуск Qt приложения.')

    if not SHOPS:
        logger.critical('Не заданы параметры магазинов')
        return None

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())



if __name__ == "__main__":
    main()
