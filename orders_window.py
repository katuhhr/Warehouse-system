from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class OrdersWindow(QWidget):
    # Сигнал для открытия формы редактирования заказа
    order_clicked = pyqtSignal(int)  # Передает order_id

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

        # Заголовок
        header_layout = QHBoxLayout()
        header_layout.addStretch()

        title = QLabel("Заказы")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setWeight(QFont.Thin)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a237e;")
        header_layout.addWidget(title)

        header_layout.addStretch()
        content_layout.addLayout(header_layout)

        # Область прокрутки для заказов
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: transparent;")

        orders_container = QWidget()
        orders_layout = QVBoxLayout()
        orders_layout.setSpacing(20)
        orders_layout.setContentsMargins(10, 0, 10, 10)

        self.orders_list = []
        orders_container.setLayout(orders_layout)
        scroll.setWidget(orders_container)

        content_layout.addWidget(scroll)

        # Кнопки внизу
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        self.add_order_button = QPushButton("Добавить")
        self.add_order_button.setStyleSheet(
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
        self.add_order_button.setCursor(Qt.PointingHandCursor)
        bottom_layout.addWidget(self.add_order_button)

        content_layout.addLayout(bottom_layout)

        # Сохраняем ссылки
        self.orders_container = orders_container
        self.orders_layout = orders_layout
        self.orders_scroll = scroll

        # Создаем контейнер для контента
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        layout.addWidget(content_widget)

        self.setLayout(layout)

        # Загружаем данные
        self.load_orders()

    def load_orders(self):
        for item in self.orders_list:
            item.setParent(None)
        self.orders_list.clear()

        orders = self.db.get_orders()

        orders_dict = {}
        for order in orders:
            order_id = order["Id"]
            if order_id not in orders_dict:
                orders_dict[order_id] = {
                    "Id": order_id,
                    "ClientId": order["ClientId"],
                    "client_name": order.get("client_name", ""),
                    "OrderDate": order.get("OrderDate", ""),
                    "Status": order.get("Status", ""),
                    "items": [],
                }
            orders_dict[order_id]["items"].append(
                {
                    "product_name": order.get("product_name", ""),
                    "Quantity": order.get("Quantity", 0),
                }
            )

        # Создаем словарь для нумерации по порядку создания (первый созданный = 1)
        all_orders_by_creation = sorted(
            orders_dict.values(),
            key=lambda x: (x.get("OrderDate", "") or "", x.get("Id", 0)),
        )
        order_number_map = {
            order["Id"]: idx + 1 for idx, order in enumerate(all_orders_by_creation)
        }

        # Разделяем заказы на активные и завершенные
        completed_orders = [
            o for o in orders_dict.values() if o.get("Status") == "Завершен"
        ]
        active_orders = [
            o for o in orders_dict.values() if o.get("Status") != "Завершен"
        ]

        # Сортируем активные заказы по дате (новые сверху - обратный порядок)
        active_orders_sorted = sorted(
            active_orders,
            key=lambda x: (x.get("OrderDate", "") or "", x.get("Id", 0)),
            reverse=True,  # Новые сверху
        )

        # Сортируем завершенные заказы по дате (новые сверху - обратный порядок)
        completed_orders_sorted = sorted(
            completed_orders,
            key=lambda x: (x.get("OrderDate", "") or "", x.get("Id", 0)),
            reverse=True,  # Новые сверху
        )

        # Объединяем: сначала активные (новые сверху), затем завершенные (новые сверху)
        sorted_orders = active_orders_sorted + completed_orders_sorted

        for order_data in sorted_orders:
            # Получаем номер заказа по порядку создания
            order_num = order_number_map.get(order_data["Id"], 0)
            order_frame = self.create_order_item(order_data, order_num)
            self.orders_layout.addWidget(order_frame)
            self.orders_list.append(order_frame)

        self.orders_layout.addStretch()

    def create_order_item(self, order, order_num):
        frame = QFrame()
        frame.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            background-color: white;
            padding: 15px;
        """
        )
        frame.setMinimumHeight(100)
        # Сохраняем order_id в frame для использования при клике
        frame.order_id = order.get("Id")

        # Делаем frame кликабельным с визуальной обратной связью
        original_style = frame.styleSheet()
        hover_style = """
            border: 2px solid #1a237e;
            border-radius: 5px;
            background-color: #e3f2fd;
            padding: 15px;
        """

        def mousePressEvent(event):
            self.on_order_clicked(frame.order_id)

        def enterEvent(event):
            frame.setStyleSheet(hover_style)

        def leaveEvent(event):
            frame.setStyleSheet(original_style)

        frame.mousePressEvent = mousePressEvent
        frame.enterEvent = enterEvent
        frame.leaveEvent = leaveEvent
        frame.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Заголовок заказа
        order_title = QLabel(f"Заказ №{order_num}")
        order_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a237e;")
        layout.addWidget(order_title)

        # Товары в заказе
        for item in order["items"]:
            product_label = QLabel(f"{item['product_name']} - {item['Quantity']} шт")
            product_label.setStyleSheet(
                "font-size: 14px; color: #1a237e; text-decoration: underline;"
            )
            product_label.setWordWrap(True)
            layout.addWidget(product_label)

        # Статус
        status_label = QLabel(f"Статус: {order.get('Status', '')}")
        status_label.setStyleSheet("font-size: 14px; color: #1a237e; margin-top: 5px;")
        layout.addWidget(status_label)

        frame.setLayout(layout)
        return frame

    def on_order_clicked(self, order_id):
        """Обработчик клика по карточке заказа"""
        self.order_clicked.emit(order_id)
