from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QScrollArea,
    QFrame,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
import os


class ProductsWindow(QWidget):
    # Сигнал для открытия формы редактирования товара
    product_clicked = pyqtSignal(int)  # Передает product_id

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setFixedSize(1000, 700)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Верхняя панель
        top_panel = QFrame()
        top_panel.setStyleSheet("padding: 5px;")
        top_panel_layout = QHBoxLayout()
        top_panel_layout.setContentsMargins(20, 5, 20, 5)
        top_panel_layout.setSpacing(15)

        # Кнопка назад
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
        top_panel_layout.addWidget(self.back_button)

        top_panel_layout.addStretch()

        top_panel.setLayout(top_panel_layout)
        layout.addWidget(top_panel)

        # Основной контент
        content_layout = QVBoxLayout()
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(30, 5, 30, 20)

        # Заголовок и поиск
        header_layout = QHBoxLayout()
        header_layout.addStretch()

        title = QLabel("Товары")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setWeight(QFont.Thin)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a237e;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск")
        self.search_input.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.search_input.setFixedWidth(300)
        header_layout.addWidget(self.search_input)

        content_layout.addLayout(header_layout)

        # Область прокрутки для товаров
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: transparent;")

        products_container = QWidget()
        products_layout = QVBoxLayout()
        products_layout.setSpacing(20)
        products_layout.setContentsMargins(10, 0, 10, 10)

        self.products_list = []
        products_container.setLayout(products_layout)
        scroll.setWidget(products_container)

        content_layout.addWidget(scroll)

        # Кнопка добавить
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        self.add_product_button = QPushButton("Добавить")
        self.add_product_button.setStyleSheet(
            """
            border: none;
            border-radius: 5px;
            padding: 12px 40px;
            background-color: #1a237e;
            color: white;
            font-size: 16px;
            font-weight: bold;
        """
        )
        self.add_product_button.setCursor(Qt.PointingHandCursor)
        bottom_layout.addWidget(self.add_product_button)

        content_layout.addLayout(bottom_layout)

        # Сохраняем ссылки
        self.products_container = products_container
        self.products_layout = products_layout
        self.products_scroll = scroll

        # Подключаем поиск
        self.search_input.textChanged.connect(self.load_products)

        # Создаем контейнер для контента
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        layout.addWidget(content_widget)

        self.setLayout(layout)

        # Загружаем данные
        self.load_products()

    def load_products(self):
        for item in self.products_list:
            item.setParent(None)
        self.products_list.clear()

        search_text = self.search_input.text()
        products = self.db.get_products(search_text)

        for product in products:
            product_frame = self.create_product_item(product)
            self.products_layout.addWidget(product_frame)
            self.products_list.append(product_frame)

        self.products_layout.addStretch()

    def create_product_item(self, product):
        frame = QFrame()
        frame.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            background-color: white;
            padding: 15px;
        """
        )
        frame.setMinimumHeight(160)
        # Сохраняем product_id в frame для использования при клике
        frame.product_id = product.get("Id")

        # Делаем frame кликабельным с визуальной обратной связью
        original_style = frame.styleSheet()
        hover_style = """
            border: 2px solid #1a237e;
            border-radius: 5px;
            background-color: #e3f2fd;
            padding: 15px;
        """

        def mousePressEvent(event):
            self.on_product_clicked(frame.product_id)

        def enterEvent(event):
            frame.setStyleSheet(hover_style)

        def leaveEvent(event):
            frame.setStyleSheet(original_style)

        frame.mousePressEvent = mousePressEvent
        frame.enterEvent = enterEvent
        frame.leaveEvent = leaveEvent
        frame.setCursor(Qt.PointingHandCursor)

        layout = QHBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(15, 15, 15, 15)

        # Изображение товара
        product_id = product.get("Id")
        image_label = QLabel()
        image_label.setFixedSize(130, 130)
        image_label.setStyleSheet(
            """
            border: 2px solid #1a237e;
            background-color: transparent;
        """
        )
        image_label.setScaledContents(True)
        image_label.setAlignment(Qt.AlignCenter)

        # Загружаем изображение по ID товара
        image_path = self.get_product_image_path(product_id)
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            # Масштабируем изображение под размер рамки
            scaled_pixmap = pixmap.scaled(
                130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            image_label.setPixmap(scaled_pixmap)

        layout.addWidget(image_label)

        # Информация о товаре
        info_layout = QVBoxLayout()
        info_layout.setSpacing(12)
        info_layout.setContentsMargins(0, 0, 0, 0)

        # Название товара
        name_label = QLabel(product.get("Name", ""))
        name_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #1a237e; padding: 5px 0px;"
        )
        name_label.setWordWrap(True)
        name_label.setMinimumHeight(30)
        info_layout.addWidget(name_label)

        # Серийный номер в отдельном поле
        serial_text = product.get("SerialNumber", "")
        serial_frame = QFrame()
        serial_frame.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            background-color: white;
            padding: 8px 12px;
        """
        )
        serial_layout = QHBoxLayout()
        serial_layout.setContentsMargins(0, 0, 0, 0)
        serial_label = QLabel(f"Серийный номер: {serial_text}")
        serial_label.setStyleSheet("font-size: 15px; color: #1a237e;")
        serial_label.setWordWrap(True)
        serial_layout.addWidget(serial_label)
        serial_frame.setLayout(serial_layout)
        info_layout.addWidget(serial_frame)

        # Количество в отдельном поле
        quantity = product.get("Quantity", 0)
        quantity_frame = QFrame()
        quantity_frame.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            background-color: white;
            padding: 8px 12px;
        """
        )
        quantity_layout = QHBoxLayout()
        quantity_layout.setContentsMargins(0, 0, 0, 0)
        quantity_label = QLabel(f"Количество: {quantity} шт")
        quantity_label.setStyleSheet("font-size: 15px; color: #1a237e;")
        quantity_layout.addWidget(quantity_label)
        quantity_frame.setLayout(quantity_layout)
        info_layout.addWidget(quantity_frame)

        info_layout.addStretch()
        layout.addLayout(info_layout, stretch=1)
        layout.addStretch()

        frame.setLayout(layout)
        return frame

    def get_product_image_path(self, product_id):
        """Возвращает путь к изображению товара по его ID"""
        # Пробуем разные расширения
        image_dir = os.path.join("images", "product")
        extensions = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]

        for ext in extensions:
            image_path = os.path.join(image_dir, f"{product_id}{ext}")
            if os.path.exists(image_path):
                return image_path

        # Если изображение не найдено, возвращаем путь к no_image
        return os.path.join(image_dir, "no_image.jpg")

    def on_product_clicked(self, product_id):
        """Обработчик клика по карточке товара"""
        self.product_clicked.emit(product_id)
