from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator


class ClientFormWindow(QWidget):
    def __init__(self, db, client_id=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.client_id = client_id
        self.setWindowTitle("Клиент")
        self.setFixedSize(700, 500)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)

        # Заголовок
        title = QLabel("Клиент")
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

        # Фамилия
        surname_layout = QHBoxLayout()
        surname_label = QLabel("Фамилия")
        surname_label.setStyleSheet("color: #1a237e; font-size: 14px; min-width: 180px; font-weight: bold;")
        self.surname_input = QLineEdit()
        self.surname_input.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        # Валидатор: только буквы (русские и латинские)
        surname_validator = QRegExpValidator(QRegExp("[а-яА-ЯёЁa-zA-Z\\s-]+"))
        self.surname_input.setValidator(surname_validator)
        self.surname_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        surname_layout.addWidget(surname_label)
        surname_layout.addWidget(self.surname_input, stretch=1)
        form_layout.addLayout(surname_layout)

        # Имя
        name_layout = QHBoxLayout()
        name_label = QLabel("Имя")
        name_label.setStyleSheet("color: black; font-size: 14px; min-width: 180px;")
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
        # Валидатор: только буквы (русские и латинские)
        name_validator = QRegExpValidator(QRegExp("[а-яА-ЯёЁa-zA-Z\\s-]+"))
        self.name_input.setValidator(name_validator)
        self.name_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input, stretch=1)
        form_layout.addLayout(name_layout)

        # Отчество
        patronymic_layout = QHBoxLayout()
        patronymic_label = QLabel("Отчество")
        patronymic_label.setStyleSheet("color: black; font-size: 14px; min-width: 180px;")
        self.patronymic_input = QLineEdit()
        self.patronymic_input.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        # Валидатор: только буквы (русские и латинские)
        patronymic_validator = QRegExpValidator(QRegExp("[а-яА-ЯёЁa-zA-Z\\s-]+"))
        self.patronymic_input.setValidator(patronymic_validator)
        self.patronymic_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        patronymic_layout.addWidget(patronymic_label)
        patronymic_layout.addWidget(self.patronymic_input, stretch=1)
        form_layout.addLayout(patronymic_layout)

        # Телефон
        phone_layout = QHBoxLayout()
        phone_label = QLabel("Телефон")
        phone_label.setStyleSheet("color: black; font-size: 14px; min-width: 180px;")
        self.phone_input = QLineEdit()
        self.phone_input.setStyleSheet(
            """
            border: 2px solid #1a237e;
            border-radius: 5px;
            padding: 8px 15px;
            background-color: white;
            color: #1a237e;
            font-size: 14px;
        """
        )
        # Валидатор: только цифры, максимум 12 символов
        phone_validator = QRegExpValidator(QRegExp("[0-9]+"))
        self.phone_input.setValidator(phone_validator)
        self.phone_input.setMaxLength(11)
        self.phone_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input, stretch=1)
        form_layout.addLayout(phone_layout)

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

        # Кнопка "Удалить" - показывается только при редактировании существующего клиента
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
        # Показываем кнопку "Удалить" только если редактируем существующего клиента
        if self.client_id:
            buttons_layout.addWidget(self.delete_button)
        else:
            self.delete_button.setVisible(False)

        # Кнопка "Изменить" - показывается только при редактировании существующего клиента
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
        # Показываем кнопку "Изменить" только если редактируем существующего клиента
        if self.client_id:
            buttons_layout.addWidget(self.edit_button)
        else:
            self.edit_button.setVisible(False)

        # Кнопка "Добавить" - показывается только при добавлении нового клиента
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
        # Показываем кнопку "Добавить" только если добавляем нового клиента
        if not self.client_id:
            buttons_layout.addWidget(self.add_button)
        else:
            self.add_button.setVisible(False)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Загружаем данные если редактируем
        if self.client_id:
            clients = self.db.get_clients()
            for client in clients:
                if client["Id"] == self.client_id:
                    self.surname_input.setText(client.get("surname", ""))
                    self.name_input.setText(client.get("name", ""))
                    self.patronymic_input.setText(client.get("patronymic", ""))
                    self.phone_input.setText(client.get("Phone", ""))
                    self.address_input.setText(client.get("Address", ""))
                    break
