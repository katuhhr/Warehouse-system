from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Авторизация")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)

        # Заголовок
        title = QLabel("Авторизация")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(32)
        title_font.setWeight(QFont.Thin)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a237e;")
        layout.addWidget(title)

        layout.addStretch()

        # Поле логина
        login_label = QLabel("Логин")
        login_label.setStyleSheet("color: #1a237e; font-size: 14px;")
        layout.addWidget(login_label)

        self.login_input = QLineEdit()
        self.login_input.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 15px;
        """
        )
        self.login_input.setMinimumWidth(350)
        layout.addWidget(self.login_input)

        # Поле пароля
        password_label = QLabel("Пароль")
        password_label.setStyleSheet("color: #1a237e; font-size: 14px;")
        layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 15px;
        """
        )
        self.password_input.setMinimumWidth(350)
        layout.addWidget(self.password_input)

        layout.addStretch()

        # Кнопка входа
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        self.login_button = QPushButton("ВХОД")
        self.login_button.setStyleSheet(
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
        self.login_button.setCursor(Qt.PointingHandCursor)
        button_layout.addWidget(self.login_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
