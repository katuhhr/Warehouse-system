from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QSizePolicy,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class BrandWindow(QWidget):
    def __init__(self, db, brand_id=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.brand_id = brand_id
        self.setWindowTitle("Марка")
        self.setFixedSize(500, 300)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 25, 30, 25)

        # Заголовок
        title = QLabel("Марка")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setWeight(QFont.Thin)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a237e;")
        layout.addWidget(title)

        layout.addStretch()

        # Выпадающий список существующих марок
        combo_layout = QHBoxLayout()
        combo_label = QLabel("Выберите марку:")
        combo_label.setStyleSheet("color: #1a237e; font-size: 14px; font-weight: bold;")
        self.brand_combo = QComboBox()
        self.brand_combo.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.brand_combo.currentIndexChanged.connect(self.on_brand_selected)
        combo_layout.addWidget(combo_label)
        combo_layout.addWidget(self.brand_combo, stretch=1)
        layout.addLayout(combo_layout)

        # Поле ввода
        input_layout = QHBoxLayout()
        name_label = QLabel("Наименование")
        name_label.setStyleSheet(
            "color: #1a237e; font-size: 14px; min-width: 150px; font-weight: bold;"
        )
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.name_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        input_layout.addWidget(name_label)
        input_layout.addWidget(self.name_input, stretch=1)
        layout.addLayout(input_layout)

        layout.addStretch()

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.back_button = QPushButton("←")
        self.back_button.setStyleSheet(
            """
            border: none;
            background-color: transparent;
            color: #1a237e;
            font-size: 24px;
            padding: 5px;
        """
        )
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setFixedSize(40, 40)
        buttons_layout.addWidget(self.back_button)

        buttons_layout.addStretch()

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setStyleSheet(
            """
            border: 2px solid #d32f2f;
            border-radius: 5px;
            padding: 10px 10px;
            background-color: #ffebee;
            color: #d32f2f;
            font-size: 16px;
            font-weight: bold;
        """
        )
        self.delete_button.setCursor(Qt.PointingHandCursor)
        self.delete_button.setMinimumWidth(120)
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_selected_brand)
        buttons_layout.addWidget(self.delete_button)

        self.edit_button = QPushButton("Изменить")
        self.edit_button.setStyleSheet(
            """
            border: none;
            border-radius: 5px;
            padding: 10px 10px;
            background-color: #1a237e;
            color: white;
            font-size: 16px;
            font-weight: bold;
        """
        )
        self.edit_button.setCursor(Qt.PointingHandCursor)
        self.edit_button.setMinimumWidth(120)
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_selected_brand)
        buttons_layout.addWidget(self.edit_button)

        self.add_button = QPushButton("Добавить")
        self.add_button.setStyleSheet(
            """
            border: none;
            border-radius: 5px;
            padding: 10px 10px;
            background-color: #1a237e;
            color: white;
            font-size: 16px;
            font-weight: bold;
        """
        )
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.add_button.setMinimumWidth(120)
        self.add_button.clicked.connect(self.add_new_brand)
        buttons_layout.addWidget(self.add_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Загружаем данные
        self.load_brands()
        self.selected_brand_id = None

        # Загружаем данные если редактируем
        if self.brand_id:
            brands = self.db.get_brands()
            for brand in brands:
                if brand["id"] == self.brand_id:
                    self.name_input.setText(brand["name"])
                    # Выбираем в комбобоксе
                    for i in range(self.brand_combo.count()):
                        if self.brand_combo.itemData(i) == self.brand_id:
                            self.brand_combo.setCurrentIndex(i)
                            break
                    break

    def load_brands(self):
        """Загружает список марок в комбобокс"""
        brands = self.db.get_brands()
        self.brand_combo.clear()
        self.brand_combo.addItem("-- Выберите марку --", None)
        for brand in brands:
            self.brand_combo.addItem(brand["name"], brand["id"])

    def on_brand_selected(self):
        """Обработчик выбора марки в комбобоксе"""
        brand_id = self.brand_combo.currentData()
        if brand_id:
            self.selected_brand_id = brand_id
            self.name_input.setText(self.brand_combo.currentText())
            self.delete_button.setEnabled(True)
            self.edit_button.setEnabled(True)
        else:
            self.selected_brand_id = None
            self.name_input.clear()
            self.delete_button.setEnabled(False)
            self.edit_button.setEnabled(False)

    def add_new_brand(self):
        """Добавляет новую марку"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите наименование марки")
            return
        try:
            self.db.add_brand(name)
            QMessageBox.information(self, "Успех", "Марка добавлена")
            self.load_brands()
            # Выбираем только что добавленную марку
            for i in range(self.brand_combo.count()):
                if self.brand_combo.itemText(i) == name:
                    self.brand_combo.setCurrentIndex(i)
                    break
            # Обновляем данные в форме товара, если она есть
            if hasattr(self, "parent_form") and hasattr(self.parent_form, "load_data"):
                self.parent_form.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении: {str(e)}")

    def edit_selected_brand(self):
        """Изменяет выбранную марку"""
        if not self.selected_brand_id:
            QMessageBox.warning(self, "Ошибка", "Выберите марку для редактирования")
            return
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите наименование марки")
            return
        try:
            self.db.update_brand(self.selected_brand_id, name)
            QMessageBox.information(self, "Успех", "Марка обновлена")
            self.load_brands()
            # Выбираем обновленную марку
            for i in range(self.brand_combo.count()):
                if self.brand_combo.itemData(i) == self.selected_brand_id:
                    self.brand_combo.setCurrentIndex(i)
                    break
            # Обновляем данные в форме товара, если она есть
            if hasattr(self, "parent_form") and hasattr(self.parent_form, "load_data"):
                self.parent_form.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении: {str(e)}")

    def delete_selected_brand(self):
        """Удаляет выбранную марку"""
        if not self.selected_brand_id:
            QMessageBox.warning(self, "Ошибка", "Выберите марку для удаления")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить марку?")
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_brand(self.selected_brand_id)
                QMessageBox.information(self, "Успех", "Марка удалена")
                self.load_brands()
                self.name_input.clear()
                self.selected_brand_id = None
                # Обновляем данные в форме товара, если она есть
                if hasattr(self, "parent_form") and hasattr(
                    self.parent_form, "load_data"
                ):
                    self.parent_form.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении: {str(e)}")
