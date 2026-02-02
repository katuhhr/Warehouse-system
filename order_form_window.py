from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QScrollArea,
    QFrame,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QDate, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator


class OrderFormWindow(QWidget):
    def __init__(self, db, order_id=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.order_id = order_id
        self.setWindowTitle("Заказ")
        self.setFixedSize(800, 700)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)

        # Заголовок
        title = QLabel("Заказ")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setWeight(QFont.Thin)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a237e;")
        layout.addWidget(title)

        # Поля формы
        form_layout = QVBoxLayout()
        form_layout.setSpacing(18)

        # Клиент
        client_layout = QHBoxLayout()
        client_label = QLabel("Клиент")
        client_label.setStyleSheet("color: #1a237e; font-size: 14px; min-width: 180px; font-weight: bold;")
        self.client_combo = QComboBox()
        self.client_combo.setEditable(True)
        self.client_combo.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.client_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        client_layout.addWidget(client_label)
        client_layout.addWidget(self.client_combo, stretch=1)
        form_layout.addLayout(client_layout)

        # Адрес
        address_layout = QHBoxLayout()
        address_label = QLabel("Адрес")
        address_label.setStyleSheet("color: black; font-size: 14px; min-width: 180px;")
        self.address_input = QLineEdit()
        self.address_input.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.address_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_input, stretch=1)
        form_layout.addLayout(address_layout)

        # Дата заказа
        date_layout = QHBoxLayout()
        date_label = QLabel("Дата заказа")
        date_label.setStyleSheet("color: black; font-size: 14px; min-width: 180px;")
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.date_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input, stretch=1)
        form_layout.addLayout(date_layout)

        # Статус заказа
        status_layout = QHBoxLayout()
        status_label = QLabel("Статус")
        status_label.setStyleSheet("color: #1a237e; font-size: 14px; min-width: 180px; font-weight: bold;")
        self.status_combo = QComboBox()
        # Статусы будут загружены из БД в методе load_data()
        self.status_combo.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.status_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_combo, stretch=1)
        form_layout.addLayout(status_layout)

        # Товары в заказе
        products_label = QLabel("Товары:")
        products_label.setStyleSheet("color: black; font-size: 16px; font-weight: bold;")
        form_layout.addWidget(products_label)

        # Область для товаров
        products_scroll = QScrollArea()
        products_scroll.setWidgetResizable(True)
        products_scroll.setFixedHeight(180)
        products_scroll.setStyleSheet(
            "border: 1px solid black; border-radius: 5px; background-color: white;"
        )

        products_container = QWidget()
        products_container_layout = QVBoxLayout()
        products_container_layout.setSpacing(5)
        products_container_layout.setContentsMargins(5, 5, 5, 5)

        self.products_list = []
        products_container.setLayout(products_container_layout)
        products_scroll.setWidget(products_container)
        form_layout.addWidget(products_scroll)

        # Добавление товара
        add_product_layout = QHBoxLayout()
        product_label = QLabel("Товар")
        product_label.setStyleSheet("color: black; font-size: 14px;")
        self.product_combo = QComboBox()
        self.product_combo.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        self.product_combo.setMaximumWidth(300)

        quantity_label = QLabel("Количество")
        quantity_label.setStyleSheet("color: black; font-size: 14px;")
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
        self.quantity_input.setFixedWidth(120)
        # Валидатор: только цифры
        quantity_validator = QRegExpValidator(QRegExp("[0-9]+"))
        self.quantity_input.setValidator(quantity_validator)

        self.add_product_button = QPushButton("+")
        self.add_product_button.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 20px;
        """
        )
        self.add_product_button.setFixedSize(45, 45)

        add_product_layout.addWidget(product_label)
        add_product_layout.addWidget(self.product_combo)
        add_product_layout.addWidget(quantity_label)
        add_product_layout.addWidget(self.quantity_input)
        add_product_layout.addWidget(self.add_product_button)
        form_layout.addLayout(add_product_layout)

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

        # Кнопка "Удалить" - показывается только при редактировании существующего заказа
        self.delete_button = QPushButton("Удалить")
        self.delete_button.setStyleSheet(
            """
            border: 2px solid #d32f2f;
            border-radius: 5px;
            padding: 12px 30px;
            background-color: #ffebee;
            color: #d32f2f;
            font-size: 16px;
            font-weight: bold;
        """
        )
        self.delete_button.setCursor(Qt.PointingHandCursor)
        # Показываем кнопку "Удалить" только если редактируем существующий заказ
        if self.order_id:
            buttons_layout.addWidget(self.delete_button)
        else:
            self.delete_button.setVisible(False)

        # Кнопка "Изменить" - показывается только при редактировании существующего заказа
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
        # Показываем кнопку "Изменить" только если редактируем существующий заказ
        if self.order_id:
            buttons_layout.addWidget(self.edit_button)
        else:
            self.edit_button.setVisible(False)

        # Кнопка "Добавить" - показывается только при создании нового заказа
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
        # Показываем кнопку "Добавить" только если создаем новый заказ
        if not self.order_id:
            buttons_layout.addWidget(self.add_button)
        else:
            self.add_button.setVisible(False)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Сохраняем ссылки
        self.products_container = products_container
        self.products_container_layout = products_container_layout

        # Загружаем данные
        self.load_data()

        # Подключаем кнопку добавления товара
        self.add_product_button.clicked.connect(self.add_product_to_order)

    def load_data(self):
        # Загружаем клиентов
        clients = self.db.get_clients()
        self.client_combo.clear()
        for client in clients:
            fio = f"{client.get('surname', '')} {client.get('name', '')} {client.get('patronymic', '')}"
            self.client_combo.addItem(fio, client["Id"])

        # Загружаем товары
        products = self.db.get_products()
        self.product_combo.clear()
        for product in products:
            self.product_combo.addItem(product.get("Name", ""), product.get("Id"))

        # Загружаем статусы из базы данных
        statuses = self.db.get_order_statuses()
        self.status_combo.clear()
        self.status_combo.addItems(statuses)

        # Если редактируем заказ, загружаем данные
        if self.order_id:
            orders = self.db.get_orders()
            for order in orders:
                if order["Id"] == self.order_id:
                    # Устанавливаем клиента
                    for i in range(self.client_combo.count()):
                        if self.client_combo.itemData(i) == order.get("ClientId"):
                            self.client_combo.setCurrentIndex(i)
                            break

                    # Устанавливаем дату
                    if order.get("OrderDate"):
                        date = QDate.fromString(str(order["OrderDate"]), "yyyy-MM-dd")
                        if date.isValid():
                            self.date_input.setDate(date)

                    # Устанавливаем статус
                    status = order.get("Status", "Создан")
                    index = self.status_combo.findText(status)
                    if index >= 0:
                        self.status_combo.setCurrentIndex(index)

                    # Загружаем товары заказа
                    order_products = self.db.get_order_products(self.order_id)
                    for op in order_products:
                        self.add_product_item(
                            op["ProductId"], op["Quantity"], op.get("product_name", "")
                        )
                    break

    def add_product_to_order(self):
        product_id = self.product_combo.currentData()
        quantity = self.quantity_input.text()
        product_name = self.product_combo.currentText()

        if product_id and quantity:
            try:
                qty = int(quantity)
                self.add_product_item(product_id, qty, product_name)
                self.quantity_input.clear()
            except ValueError:
                pass

    def add_product_item(self, product_id, quantity, product_name):
        product_frame = QFrame()
        product_frame.setStyleSheet(
            "border: 2px solid #1a237e; border-radius: 5px; padding: 10px; background-color: white;"
        )

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        label = QLabel(f"{product_name} - {quantity} шт")
        label.setStyleSheet("font-size: 14px; color: #1a237e;")
        layout.addWidget(label)

        layout.addStretch()

        remove_button = QPushButton("×")
        remove_button.setStyleSheet(
            "border: none; background-color: transparent; color: red; font-size: 18px;"
        )
        remove_button.setFixedSize(20, 20)
        remove_button.clicked.connect(lambda: self.remove_product_item(product_frame))
        layout.addWidget(remove_button)

        product_frame.setLayout(layout)
        product_frame.product_id = product_id
        product_frame.quantity = quantity

        self.products_container_layout.addWidget(product_frame)
        self.products_list.append(product_frame)

    def remove_product_item(self, frame):
        if frame in self.products_list:
            self.products_list.remove(frame)
            frame.setParent(None)
