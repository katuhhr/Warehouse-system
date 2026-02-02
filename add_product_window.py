from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator


class AddProductWindow(QWidget):
    def __init__(self, db, product_id=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.product_id = product_id
        self.setWindowTitle("Добавить товар")
        self.setFixedSize(800, 650)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 35, 40, 35)

        # Заголовок
        title = QLabel("Добавить товар")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(30)
        title_font.setWeight(QFont.Thin)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a237e;")
        layout.addWidget(title)

        # Поля формы
        form_layout = QVBoxLayout()
        form_layout.setSpacing(18)

        # Наименование
        name_layout = QHBoxLayout()
        name_label = QLabel("Наименование")
        name_label.setStyleSheet(
            "color: #1a237e; font-size: 14px; min-width: 200px; font-weight: bold;"
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
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input, stretch=1)
        form_layout.addLayout(name_layout)

        # Серийный номер
        serial_layout = QHBoxLayout()
        serial_label = QLabel("Серийный номер")
        serial_label.setStyleSheet("color: black; font-size: 14px; min-width: 200px;")
        self.serial_input = QLineEdit()
        self.serial_input.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.serial_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        serial_layout.addWidget(serial_label)
        serial_layout.addWidget(self.serial_input, stretch=1)
        form_layout.addLayout(serial_layout)

        # Марка автомобиля
        brand_layout = QHBoxLayout()
        brand_label = QLabel("Марка автомобиля")
        brand_label.setStyleSheet("color: black; font-size: 14px; min-width: 200px;")
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
        self.brand_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.brand_add_button = QPushButton("Добавить")
        self.brand_add_button.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        brand_layout.addWidget(brand_label)
        brand_layout.addWidget(self.brand_combo, stretch=1)
        brand_layout.addWidget(self.brand_add_button)
        form_layout.addLayout(brand_layout)

        # Модель автомобиля
        model_layout = QHBoxLayout()
        model_label = QLabel("Модель автомобиля")
        model_label.setStyleSheet("color: black; font-size: 14px; min-width: 200px;")
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
        self.model_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.model_add_button = QPushButton("Добавить")
        self.model_add_button.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo, stretch=1)
        model_layout.addWidget(self.model_add_button)
        form_layout.addLayout(model_layout)

        # Категория
        category_layout = QHBoxLayout()
        category_label = QLabel("Категория")
        category_label.setStyleSheet("color: black; font-size: 14px; min-width: 200px;")
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
        self.category_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.category_add_button = QPushButton("Добавить")
        self.category_add_button.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo, stretch=1)
        category_layout.addWidget(self.category_add_button)
        form_layout.addLayout(category_layout)

        # Ячейка
        cell_layout = QHBoxLayout()
        cell_label = QLabel("Ячейка")
        cell_label.setStyleSheet("color: black; font-size: 14px; min-width: 200px;")
        
        # Аллея (только A, B, C)
        self.alley_combo = QComboBox()
        self.alley_combo.addItems(["A", "B", "C"])
        self.alley_combo.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.alley_combo.setFixedWidth(80)
        
        # Разделитель
        separator_label = QLabel("-")
        separator_label.setStyleSheet("color: #1a237e; font-size: 14px; font-weight: bold;")
        separator_label.setAlignment(Qt.AlignCenter)
        separator_label.setFixedWidth(20)
        
        # Номер ячейки (цифры и дефисы)
        self.cell_number_input = QLineEdit()
        self.cell_number_input.setPlaceholderText("01-12")
        self.cell_number_input.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.cell_number_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # Валидатор для номера ячейки: только цифры и дефисы
        cell_validator = QRegExpValidator(QRegExp("[0-9\\-]+"))
        self.cell_number_input.setValidator(cell_validator)
        
        cell_layout.addWidget(cell_label)
        cell_layout.addWidget(self.alley_combo)
        cell_layout.addWidget(separator_label)
        cell_layout.addWidget(self.cell_number_input, stretch=1)
        form_layout.addLayout(cell_layout)

        # Количество
        quantity_layout = QHBoxLayout()
        quantity_label = QLabel("Количество")
        quantity_label.setStyleSheet("color: black; font-size: 14px; min-width: 200px;")
        self.quantity_input = QLineEdit()
        self.quantity_input.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.quantity_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # Валидатор для количества: только цифры
        quantity_validator = QRegExpValidator(QRegExp("[0-9]+"))
        self.quantity_input.setValidator(quantity_validator)
        quantity_layout.addWidget(quantity_label)
        quantity_layout.addWidget(self.quantity_input, stretch=1)
        form_layout.addLayout(quantity_layout)

        layout.addLayout(form_layout)
        layout.addStretch()

        # Кнопки внизу
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

        # Кнопки для редактирования существующего товара
        if self.product_id:
            self.delete_button = QPushButton("Удалить")
            self.delete_button.setStyleSheet(
                """
                border: 2px solid #d32f2f;
                border-radius: 5px;
                padding: 10px 25px;
                background-color: #ffebee;
                color: #d32f2f;
                font-size: 14px;
                font-weight: bold;
            """
            )
            self.delete_button.setCursor(Qt.PointingHandCursor)
            buttons_layout.addWidget(self.delete_button)

            self.edit_button = QPushButton("Изменить")
            self.edit_button.setStyleSheet(
                """
                border: none;
                border-radius: 5px;
                padding: 12px 30px;
                background-color: #1a237e;
                color: white;
                font-size: 16px;
                font-weight: bold;
            """
            )
            self.edit_button.setCursor(Qt.PointingHandCursor)
            buttons_layout.addWidget(self.edit_button)
        else:
            # Кнопка для создания нового товара
            self.add_button = QPushButton("Добавить")
            self.add_button.setStyleSheet(
                """
                border: none;
                border-radius: 5px;
                padding: 12px 30px;
                background-color: #1a237e;
                color: white;
                font-size: 16px;
                font-weight: bold;
            """
            )
            self.add_button.setCursor(Qt.PointingHandCursor)
            buttons_layout.addWidget(self.add_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Загружаем данные
        self.load_data()

        # Обновляем модели при изменении марки
        self.brand_combo.currentIndexChanged.connect(self.update_models)

    def load_data(self):
        # Загружаем марки
        brands = self.db.get_brands()
        self.brand_combo.clear()
        for brand in brands:
            self.brand_combo.addItem(brand["name"], brand["id"])

        # Загружаем категории
        categories = self.db.get_categories()
        self.category_combo.clear()
        for category in categories:
            self.category_combo.addItem(category["name"], category["id"])

        # Загружаем модели
        self.update_models()

        # Если редактируем товар, загружаем данные
        if self.product_id:
            products = self.db.get_products()
            for product in products:
                if product.get("Id") == self.product_id:
                    self.name_input.setText(product.get("Name", ""))
                    self.serial_input.setText(product.get("SerialNumber", ""))
                    self.quantity_input.setText(str(product.get("Quantity", 0)))

                    # Устанавливаем марку
                    for i in range(self.brand_combo.count()):
                        if self.brand_combo.itemData(i) == product.get("brand_id"):
                            self.brand_combo.setCurrentIndex(i)
                            break

                    # Обновляем модели и устанавливаем модель
                    self.update_models()
                    for i in range(self.model_combo.count()):
                        if self.model_combo.itemData(i) == product.get("model_id"):
                            self.model_combo.setCurrentIndex(i)
                            break

                    # Устанавливаем категорию
                    for i in range(self.category_combo.count()):
                        if self.category_combo.itemData(i) == product.get(
                            "category_id"
                        ):
                            self.category_combo.setCurrentIndex(i)
                            break

                    # Загружаем ячейку
                    cell_code = self.db.get_product_cell_code(self.product_id)
                    if cell_code:
                        # Разбираем код ячейки: первая буква - аллея, остальное - номер
                        alley = cell_code[0].upper()
                        cell_number = cell_code[1:] if len(cell_code) > 1 else ""
                        # Убираем дефис в начале, если есть
                        if cell_number.startswith("-"):
                            cell_number = cell_number[1:]
                        
                        # Устанавливаем аллею
                        # Преобразуем кириллицу в латиницу, если нужно (для обратной совместимости)
                        if alley == "А":
                            alley = "A"
                        elif alley == "Б":
                            alley = "B"
                        elif alley == "В":
                            alley = "C"
                        
                        index = self.alley_combo.findText(alley)
                        if index >= 0:
                            self.alley_combo.setCurrentIndex(index)
                        
                        # Устанавливаем номер ячейки
                        self.cell_number_input.setText(cell_number)
                    break

    def update_models(self):
        brand_id = self.brand_combo.currentData()
        if brand_id:
            models = self.db.get_models(brand_id)
            self.model_combo.clear()
            for model in models:
                self.model_combo.addItem(model["name"], model["id"])
