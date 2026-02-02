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
from PyQt5.QtGui import QFont


class ClientsWindow(QWidget):
    # Сигнал для открытия формы редактирования клиента
    client_clicked = pyqtSignal(int)  # Передает client_id

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

        title = QLabel("Клиенты")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setWeight(QFont.Thin)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a237e;")
        header_layout.addWidget(title)

        header_layout.addStretch()
        content_layout.addLayout(header_layout)

        # Область прокрутки для клиентов
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: transparent;")

        clients_container = QWidget()
        clients_layout = QVBoxLayout()
        clients_layout.setSpacing(15)
        clients_layout.setContentsMargins(10, 0, 10, 10)

        self.clients_list = []
        clients_container.setLayout(clients_layout)
        scroll.setWidget(clients_container)

        content_layout.addWidget(scroll)

        # Кнопка добавить
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        self.add_client_button = QPushButton("Добавить")
        self.add_client_button.setStyleSheet(
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
        self.add_client_button.setCursor(Qt.PointingHandCursor)
        bottom_layout.addWidget(self.add_client_button)

        content_layout.addLayout(bottom_layout)

        # Сохраняем ссылки
        self.clients_container = clients_container
        self.clients_layout = clients_layout
        self.clients_scroll = scroll

        # Создаем контейнер для контента
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        layout.addWidget(content_widget)

        self.setLayout(layout)

        # Загружаем данные
        self.load_clients()

    def load_clients(self):
        for item in self.clients_list:
            item.setParent(None)
        self.clients_list.clear()

        clients = self.db.get_clients()

        # Создаем словарь для нумерации по порядку создания (первый созданный = 1)
        # Клиенты уже отсортированы по ID в базе данных
        client_number_map = {
            client["Id"]: idx + 1 for idx, client in enumerate(clients)
        }

        for client in clients:
            # Получаем номер клиента по порядку создания
            client_num = client_number_map.get(client["Id"], 0)
            client_frame = self.create_client_item(client, client_num)
            self.clients_layout.addWidget(client_frame)
            self.clients_list.append(client_frame)

        self.clients_layout.addStretch()

    def create_client_item(self, client, number):
        frame = QFrame()
        frame.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            background-color: white;
            padding: 10px;
        """
        )
        frame.setFixedHeight(80)
        # Сохраняем client_id в frame для использования при клике
        frame.client_id = client.get("Id")

        # Делаем frame кликабельным с визуальной обратной связью
        original_style = frame.styleSheet()
        hover_style = """
            border: 2px solid #1a237e;
            border-radius: 5px;
            background-color: #e3f2fd;
            padding: 10px;
        """

        def mousePressEvent(event):
            self.on_client_clicked(frame.client_id)

        frame.mousePressEvent = mousePressEvent
        frame.setCursor(Qt.PointingHandCursor)

        layout = QHBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 10, 15, 10)

        # Номер в отдельном поле
        number_frame = QFrame()
        number_frame_original_style = """
            border: none;
            background-color: white;
            padding: 10px 15px;
        """
        number_frame_hover_style = """
            border: none;
            background-color: #e3f2fd;
            padding: 10px 15px;
        """
        number_frame.setStyleSheet(number_frame_original_style)
        number_frame.setFixedWidth(100)
        number_frame.setFixedHeight(55)
        number_layout = QHBoxLayout()
        number_layout.setContentsMargins(0, 0, 0, 0)
        number_label = QLabel(str(number))
        number_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #1a237e;"
        )
        number_label.setAlignment(Qt.AlignCenter)
        number_layout.addWidget(number_label)
        number_frame.setLayout(number_layout)
        layout.addWidget(number_frame)

        # ФИО
        surname = client.get("surname") or ""
        name = client.get("name") or ""
        patronymic = client.get("patronymic") or ""
        fio = f"{surname}.{name[:1] if name else ''}.{patronymic[:1] if patronymic else ''}"
        fio_label = QLineEdit(fio)
        fio_label.setReadOnly(True)
        fio_label.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 12px 20px;
            background-color: white;
            color: #1a237e;
            font-size: 16px;
            font-weight: bold;
        """
        )
        fio_label.setMinimumHeight(50)
        fio_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(fio_label, stretch=1)

        layout.addStretch()

        # Обновляем обработчики событий для подсветки number_frame
        def enterEvent(event):
            frame.setStyleSheet(hover_style)
            number_frame.setStyleSheet(number_frame_hover_style)

        def leaveEvent(event):
            frame.setStyleSheet(original_style)
            number_frame.setStyleSheet(number_frame_original_style)

        frame.enterEvent = enterEvent
        frame.leaveEvent = leaveEvent

        frame.setLayout(layout)
        return frame

    def on_client_clicked(self, client_id):
        """Обработчик клика по карточке клиента"""
        self.client_clicked.emit(client_id)
