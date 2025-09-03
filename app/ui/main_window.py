import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from loguru import logger

from app.config import SHOPS
from app.services.product_manager import change_product_rest
from app.services.price_updater import update_prices
from app.ui.shops_block import ShopBlock


class MainWindow(QWidget):

    def __init__(self) -> None:

        logger.debug('Инициализация главного окна')

        super().__init__()
        self.setWindowTitle("Wildberries Manager")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self._create_top_bar()

        self.shop_blocks: dict[str, ShopBlock] = {}
        for shop in SHOPS:
            shop_block = ShopBlock(shop)
            self.shop_blocks[shop] = shop_block
            self.main_layout.addWidget(shop_block)

            shop_block.btn_update.clicked.connect(
                lambda checked, s=shop: self.process_prices(s)
            )
            shop_block.btn_change.clicked.connect(
                lambda checked, s=shop: self.process_change(s)
            )

        self.add_logo()

    def _create_top_bar(self) -> None:

        top_bar = QFrame()
        top_bar.setStyleSheet("background-color: #0078d7; color: white;")
        top_bar.setFixedHeight(40)
        
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 0, 10, 0)
        
        top_label = QLabel("Markines Repricer")
        top_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        top_layout.addWidget(top_label)
        top_layout.addStretch()
        top_bar.setLayout(top_layout)
        
        self.main_layout.addWidget(top_bar)

    def add_logo(self) -> None:

        self.main_layout.addStretch()
        
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_path = str(
            Path(__file__).parent.parent / 'images' / 'markines_image.png'
        )

        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                logo_label.setPixmap(pixmap)
            else:
                logo_label.setText("Не удалось загрузить логотип")
        else:
            logo_label.setText("Логотип не найден")

        self.main_layout.addWidget(logo_label)

    def process_prices(self, shop: str) -> None:

        logger.info('Начинаю изменять цены...')

        shop_block = self.shop_blocks[shop]
        path = shop_block.selected_path
        
        if not path:
            QMessageBox.information(
                self,
                "Ошибка", f"Файл для магазина '{shop}' не выбран."
            )
            return

        api_key = SHOPS[shop]
        result = update_prices(api_key, path)
        
        if result:
            QMessageBox.information(
                self,
                "Обновление цен", f"Успешно: {result[0]}, Ошибок: {result[1]}"
            )
        else:
            QMessageBox.information(self, "Обновление цен", "Нет данных.")

        shop_block.btn_update.setDisabled(True)
        shop_block.btn_change.setDisabled(True)

    def process_change(self, shop: str) -> None:

        shop_block = self.shop_blocks[shop]
        path = shop_block.selected_path

        if not path:
            QMessageBox.information(
                self,
                "Ошибка",
                f"Файл для магазина '{shop}' не выбран."
            )
            return

        api_key = SHOPS[shop]
        _, message = change_product_rest(api_key, path)

        QMessageBox.information(
            self,
            "Изменение остатков товаров",
            message if message else "Все прошло успешно."
        )

        shop_block.btn_update.setDisabled(True)
        shop_block.btn_change.setDisabled(True)
