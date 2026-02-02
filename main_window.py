from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Главная")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)

        # Верхняя часть с кнопкой назад
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

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
        top_layout.addWidget(self.back_button)
        top_layout.addStretch()

        layout.addLayout(top_layout)

        # Заголовок
        title = QLabel("Главная")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(32)
        title_font.setWeight(QFont.Thin)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a237e;")
        layout.addWidget(title)

        layout.addStretch()

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        self.products_button = QPushButton("Товары")
        self.products_button.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 18px 3px;
            background-color: white;
            color: #1a237e;
            font-size: 16px;
            font-weight: bold;
        """
        )
        self.products_button.setCursor(Qt.PointingHandCursor)
        buttons_layout.addWidget(self.products_button)

        self.orders_button = QPushButton("Заказы")
        self.orders_button.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 18px 3px;
            background-color: white;
            color: #1a237e;
            font-size: 16px;
            font-weight: bold;
        """
        )
        self.orders_button.setCursor(Qt.PointingHandCursor)
        buttons_layout.addWidget(self.orders_button)

        self.clients_button = QPushButton("Клиенты")
        self.clients_button.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 18px 3px;
            background-color: white;
            color: #1a237e;
            font-size: 16px;
            font-weight: bold;
        """
        )
        self.clients_button.setCursor(Qt.PointingHandCursor)
        buttons_layout.addWidget(self.clients_button)

        layout.addLayout(buttons_layout)

        layout.addStretch()

        self.setLayout(layout)
