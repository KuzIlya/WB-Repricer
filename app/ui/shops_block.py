import os

import pandas as pd
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QFileDialog, QFrame, QMessageBox
from PyQt6.QtCore import pyqtSlot, QMetaObject


class ShopBlock(QFrame):

    def __init__(self, shop_name: str) -> None:
        super().__init__()

        self.shop_name = shop_name
        self.selected_path: str | None = None

        self.setStyleSheet("background-color: #0078d7; color: white;")
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        self.__create_shop_label(layout)
        self.__create_file_label()
        self.__create_file_button()
        self.__create_update_button()
        self.__create_change_button()

        layout.addWidget(self.shop_label)
        layout.addWidget(self.btn_file)
        layout.addWidget(self.file_label)
        layout.addStretch()
        layout.addWidget(self.btn_update)
        layout.addWidget(self.btn_change)

        self.setLayout(layout)

        QMetaObject.connectSlotsByName(self)

    def __create_shop_label(self, layout: QHBoxLayout) -> None:
        self.shop_label = QLabel(self.shop_name)
        self.shop_label.setStyleSheet("font-weight: bold; font-size: 14px;")

    def __create_file_label(self) -> None:
        self.file_label = QLabel("Файл не выбран")
        self.file_label.setStyleSheet("color: white; font-style: italic; margin-left: 10px;")
        self.file_label.setFixedWidth(200)

    def __create_file_button(self) -> None:
        self.btn_file = QPushButton("Выбрать файл")
        self.btn_file.setObjectName("btn_file")  
        self.btn_file.setToolTip("Выбрать Excel-файл")
        self.btn_file.setStyleSheet("background-color: white; color: #0078d7; padding: 5px 10px;")

    def __create_update_button(self) -> None:
        self.btn_update = QPushButton("Обновить цены")
        self.btn_update.setObjectName("btn_update")
        self.btn_update.setEnabled(False)
        self.__set_button_style(self.btn_update)

    def __create_change_button(self) -> None:
        self.btn_change = QPushButton("Изменить остатки")
        self.btn_change.setObjectName("btn_change")
        self.btn_change.setEnabled(False)
        self.__set_button_style(self.btn_change)

    def __set_button_style(self, button: QPushButton) -> None:
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #0078d7;
                padding: 5px 15px;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

    @pyqtSlot()
    def on_btn_file_clicked(self):

        path, _ = QFileDialog.getOpenFileName(
            None,
            f"Выберите файл для {self.shop_name}",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        
        if path:
            try:
                df = pd.read_excel(path)
                num_columns = len(df.columns)

                self.selected_path = path
                file_name = os.path.basename(path)
                self.file_label.setText(f"{file_name} - {num_columns} {'колонка' if num_columns == 1 else 'колонки'}")

                if num_columns == 1:
                    self.btn_change.setEnabled(True)
                    self.btn_update.setEnabled(False)
                elif num_columns == 2:
                    self.btn_update.setEnabled(True)
                    self.btn_change.setEnabled(True)
                else:
                    self.btn_change.setEnabled(False)
                    self.btn_update.setEnabled(False)
                    QMessageBox.critical(None, "Ошибка", "Формат Excel-файла не поддерживается.")
            except Exception as e:
                QMessageBox.critical(None, "Ошибка", f"Не удалось обработать файл:\n{str(e)}")
