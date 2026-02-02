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


class ModelWindow(QWidget):
    def __init__(self, db, model_id=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.model_id = model_id
        self.parent_window = parent  # Сохраняем ссылку на родительское окно
        self.setWindowTitle("Модель")
        self.setFixedSize(500, 300)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 25, 30, 25)

        # Заголовок
        title = QLabel("Модель")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setWeight(QFont.Thin)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a237e;")
        layout.addWidget(title)

        layout.addStretch()

        # Выпадающий список существующих моделей
        combo_layout = QHBoxLayout()
        combo_label = QLabel("Выберите модель:")
        combo_label.setStyleSheet("color: #1a237e; font-size: 14px; font-weight: bold;")
        self.model_combo = QComboBox()
        self.model_combo.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.model_combo.currentIndexChanged.connect(self.on_model_selected)
        combo_layout.addWidget(combo_label)
        combo_layout.addWidget(self.model_combo, stretch=1)
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
        self.delete_button.clicked.connect(self.delete_selected_model)
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
        self.edit_button.clicked.connect(self.edit_selected_model)
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
        self.add_button.clicked.connect(self.add_new_model)
        buttons_layout.addWidget(self.add_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Загружаем данные
        self.load_models()
        self.selected_model_id = None

        # Загружаем данные если редактируем
        if self.model_id:
            models = self.db.get_models()
            for model in models:
                if model["id"] == self.model_id:
                    self.name_input.setText(model["name"])
                    # Выбираем в комбобоксе
                    for i in range(self.model_combo.count()):
                        if self.model_combo.itemData(i) == self.model_id:
                            self.model_combo.setCurrentIndex(i)
                            break
                    break

    def load_models(self):
        """Загружает список моделей в комбобокс"""
        models = self.db.get_models()
        self.model_combo.clear()
        self.model_combo.addItem("-- Выберите модель --", None)
        for model in models:
            self.model_combo.addItem(model["name"], model["id"])

    def on_model_selected(self):
        """Обработчик выбора модели в комбобоксе"""
        model_id = self.model_combo.currentData()
        if model_id:
            self.selected_model_id = model_id
            self.name_input.setText(self.model_combo.currentText())
            self.delete_button.setEnabled(True)
            self.edit_button.setEnabled(True)
        else:
            self.selected_model_id = None
            self.name_input.clear()
            self.delete_button.setEnabled(False)
            self.edit_button.setEnabled(False)

    def add_new_model(self):
        """Добавляет новую модель"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите наименование модели")
            return

        # Получаем brand_id из родительского окна (формы товара)
        brand_id = None
        if self.parent_window and hasattr(self.parent_window, "brand_combo"):
            brand_id = self.parent_window.brand_combo.currentData()

        if not brand_id:
            QMessageBox.warning(
                self, "Ошибка", "Выберите марку в форме товара перед добавлением модели"
            )
            return

        try:
            self.db.add_model(name, brand_id)
            QMessageBox.information(self, "Успех", "Модель добавлена")
            self.load_models()
            # Выбираем только что добавленную модель
            for i in range(self.model_combo.count()):
                if self.model_combo.itemText(i) == name:
                    self.model_combo.setCurrentIndex(i)
                    break
            # Обновляем данные в форме товара, если она есть
            if hasattr(self, "parent_form") and hasattr(self.parent_form, "load_data"):
                self.parent_form.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении: {str(e)}")

    def edit_selected_model(self):
        """Изменяет выбранную модель"""
        if not self.selected_model_id:
            QMessageBox.warning(self, "Ошибка", "Выберите модель для редактирования")
            return
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите наименование модели")
            return

        # Получаем brand_id из родительского окна (формы товара)
        brand_id = None
        if self.parent_window and hasattr(self.parent_window, "brand_combo"):
            brand_id = self.parent_window.brand_combo.currentData()

        if not brand_id:
            QMessageBox.warning(
                self, "Ошибка", "Выберите марку в форме товара перед изменением модели"
            )
            return

        try:
            self.db.update_model(self.selected_model_id, name, brand_id)
            QMessageBox.information(self, "Успех", "Модель обновлена")
            self.load_models()
            # Выбираем обновленную модель
            for i in range(self.model_combo.count()):
                if self.model_combo.itemData(i) == self.selected_model_id:
                    self.model_combo.setCurrentIndex(i)
                    break
            # Обновляем данные в форме товара, если она есть
            if hasattr(self, "parent_form") and hasattr(self.parent_form, "load_data"):
                self.parent_form.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении: {str(e)}")

    def delete_selected_model(self):
        """Удаляет выбранную модель"""
        if not self.selected_model_id:
            QMessageBox.warning(self, "Ошибка", "Выберите модель для удаления")
            return
        reply = QMessageBox.question(self, "Подтверждение", "Удалить модель?")
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_model(self.selected_model_id)
                QMessageBox.information(self, "Успех", "Модель удалена")
                self.load_models()
                self.name_input.clear()
                self.selected_model_id = None
                # Обновляем данные в форме товара, если она есть
                if hasattr(self, "parent_form") and hasattr(
                    self.parent_form, "load_data"
                ):
                    self.parent_form.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении: {str(e)}")
