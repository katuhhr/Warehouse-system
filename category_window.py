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


class CategoryWindow(QWidget):
    def __init__(self, db, category_id=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.category_id = category_id
        self.setWindowTitle("Категория")
        self.setFixedSize(500, 300)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 25, 30, 25)

        # Заголовок
        title = QLabel("Категория")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setWeight(QFont.Thin)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a237e;")
        layout.addWidget(title)

        layout.addStretch()

        # Выпадающий список существующих категорий
        combo_layout = QHBoxLayout()
        combo_label = QLabel("Выберите категорию:")
        combo_label.setStyleSheet("color: #1a237e; font-size: 14px; font-weight: bold;")
        self.category_combo = QComboBox()
        self.category_combo.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.category_combo.currentIndexChanged.connect(self.on_category_selected)
        combo_layout.addWidget(combo_label)
        combo_layout.addWidget(self.category_combo, stretch=1)
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
        self.delete_button.clicked.connect(self.delete_selected_category)
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
        self.edit_button.clicked.connect(self.edit_selected_category)
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
        self.add_button.clicked.connect(self.add_new_category)
        buttons_layout.addWidget(self.add_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Загружаем данные
        self.load_categories()
        self.selected_category_id = None

        # Загружаем данные если редактируем
        if self.category_id:
            categories = self.db.get_categories()
            for category in categories:
                if category["id"] == self.category_id:
                    self.name_input.setText(category["name"])
                    # Выбираем в комбобоксе
                    for i in range(self.category_combo.count()):
                        if self.category_combo.itemData(i) == self.category_id:
                            self.category_combo.setCurrentIndex(i)
                            break
                    break

    def load_categories(self):
        """Загружает список категорий в комбобокс"""
        categories = self.db.get_categories()
        self.category_combo.clear()
        self.category_combo.addItem("-- Выберите категорию --", None)
        for category in categories:
            self.category_combo.addItem(category["name"], category["id"])

    def on_category_selected(self):
        """Обработчик выбора категории в комбобоксе"""
        category_id = self.category_combo.currentData()
        if category_id:
            self.selected_category_id = category_id
            self.name_input.setText(self.category_combo.currentText())
            self.delete_button.setEnabled(True)
            self.edit_button.setEnabled(True)
        else:
            self.selected_category_id = None
            self.name_input.clear()
            self.delete_button.setEnabled(False)
            self.edit_button.setEnabled(False)

    def add_new_category(self):
        """Добавляет новую категорию"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите наименование категории")
            return
        try:
            self.db.add_category(name)
            QMessageBox.information(self, "Успех", "Категория добавлена")
            self.load_categories()
            # Выбираем только что добавленную категорию
            for i in range(self.category_combo.count()):
                if self.category_combo.itemText(i) == name:
                    self.category_combo.setCurrentIndex(i)
                    break
            # Обновляем данные в форме товара, если она есть
            if hasattr(self, "parent_form") and hasattr(self.parent_form, "load_data"):
                self.parent_form.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении: {str(e)}")

    def edit_selected_category(self):
        """Изменяет выбранную категорию"""
        if not self.selected_category_id:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для редактирования")
            return
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите наименование категории")
            return
        try:
            self.db.update_category(self.selected_category_id, name)
            QMessageBox.information(self, "Успех", "Категория обновлена")
            self.load_categories()
            # Выбираем обновленную категорию
            for i in range(self.category_combo.count()):
                if self.category_combo.itemData(i) == self.selected_category_id:
                    self.category_combo.setCurrentIndex(i)
                    break
            # Обновляем данные в форме товара, если она есть
            if hasattr(self, "parent_form") and hasattr(self.parent_form, "load_data"):
                self.parent_form.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении: {str(e)}")

    def delete_selected_category(self):
        """Удаляет выбранную категорию"""
        if not self.selected_category_id:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для удаления")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить категорию?")
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_category(self.selected_category_id)
                QMessageBox.information(self, "Успех", "Категория удалена")
                self.load_categories()
                self.name_input.clear()
                self.selected_category_id = None
                # Обновляем данные в форме товара, если она есть
                if hasattr(self, "parent_form") and hasattr(
                    self.parent_form, "load_data"
                ):
                    self.parent_form.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении: {str(e)}")
