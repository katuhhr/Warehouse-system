import sys
from PyQt5.QtWidgets import (
    QApplication,
    QStackedWidget,
    QMessageBox,
    QDesktopWidget,
    QPushButton,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
from database import Database
from login_window import LoginWindow
from main_window import MainWindow
from products_window import ProductsWindow
from clients_window import ClientsWindow
from orders_window import OrdersWindow
from add_product_window import AddProductWindow
from brand_window import BrandWindow
from model_window import ModelWindow
from category_window import CategoryWindow
from client_form_window import ClientFormWindow
from order_form_window import OrderFormWindow


class AppController:
    def __init__(self):
        self.db = Database()
        self.stacked_widget = QStackedWidget()
        # Хранилище для окон марки, модели и категории, чтобы они не удалялись сборщиком мусора
        self._brand_window = None
        self._model_window = None
        self._category_window = None

        # Создаем окна
        self.login_window = LoginWindow()
        self.main_window = MainWindow()
        self.products_window = ProductsWindow(self.db)
        self.clients_window = ClientsWindow(self.db)
        self.orders_window = OrdersWindow(self.db)

        # Добавляем окна в стек
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.main_window)
        self.stacked_widget.addWidget(self.products_window)
        self.stacked_widget.addWidget(self.clients_window)
        self.stacked_widget.addWidget(self.orders_window)

        # Подключаем сигналы
        self.setup_connections()

        # Начинаем с окна авторизации
        self.stacked_widget.setCurrentWidget(self.login_window)
        self.update_stacked_widget_size()
        self.center_window(self.stacked_widget)

    def center_window(self, window):
        """Центрирует окно на экране"""
        frame_geometry = window.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        window.move(frame_geometry.topLeft())

    def update_stacked_widget_size(self):
        """Обновляет размер QStackedWidget в соответствии с текущим окном"""
        current_widget = self.stacked_widget.currentWidget()
        if current_widget:
            size = current_widget.size()
            self.stacked_widget.setFixedSize(size)

    def setup_connections(self):
        # Авторизация
        self.login_window.login_button.clicked.connect(self.handle_login)

        # Главное окно
        self.main_window.back_button.clicked.connect(self.go_to_login)
        self.main_window.products_button.clicked.connect(self.go_to_products)
        self.main_window.orders_button.clicked.connect(self.go_to_orders)
        self.main_window.clients_button.clicked.connect(self.go_to_clients)

        # Окна товаров, клиентов и заказов
        self.products_window.back_button.clicked.connect(self.go_to_main)
        self.products_window.add_product_button.clicked.connect(self.show_add_product)
        self.products_window.product_clicked.connect(self.show_edit_product)

        self.clients_window.back_button.clicked.connect(self.go_to_main)
        self.clients_window.add_client_button.clicked.connect(self.show_add_client)
        self.clients_window.client_clicked.connect(self.show_edit_client)

        self.orders_window.back_button.clicked.connect(self.go_to_main)
        self.orders_window.add_order_button.clicked.connect(self.show_add_order)
        self.orders_window.order_clicked.connect(self.show_edit_order_by_id)

    def handle_login(self):
        login = self.login_window.login_input.text()
        password = self.login_window.password_input.text()

        # Проверка логина и пароля
        if login == "admin" and password == "admin123":
            self.stacked_widget.setCurrentWidget(self.main_window)
            self.update_stacked_widget_size()
            self.center_window(self.stacked_widget)
        else:
            QMessageBox.warning(
                self.login_window, "Ошибка", "Неверный логин или пароль"
            )

    def go_to_login(self):
        self.stacked_widget.setCurrentWidget(self.login_window)
        self.update_stacked_widget_size()
        self.login_window.login_input.clear()
        self.login_window.password_input.clear()

    def go_to_products(self):
        """Переходит на окно товаров"""
        self.stacked_widget.setCurrentWidget(self.products_window)
        self.update_stacked_widget_size()
        self.center_window(self.stacked_widget)
        self.products_window.load_products()

    def go_to_orders(self):
        """Переходит на окно заказов"""
        self.stacked_widget.setCurrentWidget(self.orders_window)
        self.update_stacked_widget_size()
        self.center_window(self.stacked_widget)
        self.orders_window.load_orders()

    def go_to_clients(self):
        """Переходит на окно клиентов"""
        self.stacked_widget.setCurrentWidget(self.clients_window)
        self.update_stacked_widget_size()
        self.center_window(self.stacked_widget)
        self.clients_window.load_clients()

    def go_to_main(self):
        """Переходит на главное окно"""
        self.stacked_widget.setCurrentWidget(self.main_window)
        self.update_stacked_widget_size()
        self.center_window(self.stacked_widget)

    def show_add_product(self):
        window = AddProductWindow(self.db)
        window.back_button.clicked.connect(window.close)
        window.add_button.clicked.connect(lambda: self.save_product(window))
        window.brand_add_button.clicked.connect(lambda: self.show_brand_window(window))
        window.model_add_button.clicked.connect(lambda: self.show_model_window(window))
        window.category_add_button.clicked.connect(
            lambda: self.show_category_window(window)
        )
        self.center_window(window)
        window.show()

    def show_edit_product(self, product_id):
        """Открывает форму редактирования товара"""
        window = AddProductWindow(self.db, product_id)
        window.back_button.clicked.connect(window.close)
        window.edit_button.clicked.connect(lambda: self.update_product(window))
        window.delete_button.clicked.connect(lambda: self.delete_product(window))
        window.brand_add_button.clicked.connect(lambda: self.show_brand_window(window))
        window.model_add_button.clicked.connect(lambda: self.show_model_window(window))
        window.category_add_button.clicked.connect(
            lambda: self.show_category_window(window)
        )
        self.center_window(window)
        window.show()

    def show_add_client(self):
        window = ClientFormWindow(self.db)
        window.back_button.clicked.connect(window.close)
        window.add_button.clicked.connect(lambda: self.save_client(window))
        self.center_window(window)
        window.show()

    def show_edit_client(self, client_id):
        """Открывает форму редактирования клиента"""
        window = ClientFormWindow(self.db, client_id)
        window.back_button.clicked.connect(window.close)
        window.edit_button.clicked.connect(lambda: self.update_client(window))
        window.delete_button.clicked.connect(lambda: self.delete_client(window))
        self.center_window(window)
        window.show()

    def show_add_order(self):
        window = OrderFormWindow(self.db)
        window.back_button.clicked.connect(window.close)
        window.add_button.clicked.connect(lambda: self.save_order(window))
        self.center_window(window)
        window.show()

    def show_edit_order_by_id(self, order_id):
        """Открывает форму редактирования заказа по ID"""
        window = OrderFormWindow(self.db, order_id)
        window.back_button.clicked.connect(window.close)
        window.edit_button.clicked.connect(lambda: self.update_order(window, order_id))
        window.delete_button.clicked.connect(
            lambda: self.delete_order(window, order_id)
        )
        self.center_window(window)
        window.show()

    def show_brand_window(self, parent_window):
        # Закрываем предыдущее окно, если оно открыто
        if self._brand_window is not None:
            self._brand_window.close()
        window = BrandWindow(self.db, parent=None)
        window.parent_form = parent_window
        window.back_button.clicked.connect(window.close)
        self._brand_window = window  # Сохраняем ссылку
        self.center_window(window)
        window.show()

    def show_model_window(self, parent_window):
        # Закрываем предыдущее окно, если оно открыто
        if self._model_window is not None:
            self._model_window.close()
        window = ModelWindow(self.db, parent=None)
        window.parent_window = parent_window
        window.parent_form = parent_window
        window.back_button.clicked.connect(window.close)
        self._model_window = window  # Сохраняем ссылку
        self.center_window(window)
        window.show()

    def show_category_window(self, parent_window):
        # Закрываем предыдущее окно, если оно открыто
        if self._category_window is not None:
            self._category_window.close()
        window = CategoryWindow(self.db, parent=None)
        window.parent_form = parent_window
        window.back_button.clicked.connect(window.close)
        self._category_window = window  # Сохраняем ссылку
        self.center_window(window)
        window.show()

    def save_product(self, window):
        try:
            name = window.name_input.text()
            serial = window.serial_input.text()
            quantity = int(window.quantity_input.text())
            brand_id = window.brand_combo.currentData()
            model_id = window.model_combo.currentData()
            category_id = window.category_combo.currentData()
            # Собираем код ячейки из аллеи и номера
            alley = window.alley_combo.currentText()
            cell_number = window.cell_number_input.text()
            cell_code = f"{alley}-{cell_number}" if cell_number else ""

            if not all([name, serial, brand_id, model_id, category_id]):
                QMessageBox.warning(window, "Ошибка", "Заполните все поля")
                return

            self.db.add_product(
                serial, name, quantity, brand_id, model_id, category_id, cell_code
            )
            QMessageBox.information(window, "Успех", "Товар добавлен")
            window.close()
            self.products_window.load_products()
        except Exception as e:
            QMessageBox.critical(window, "Ошибка", f"Ошибка при сохранении: {str(e)}")

    def update_product(self, window):
        if not window.product_id:
            QMessageBox.warning(window, "Ошибка", "Товар не выбран для редактирования")
            return

        try:
            name = window.name_input.text()
            serial = window.serial_input.text()
            quantity = int(window.quantity_input.text())
            brand_id = window.brand_combo.currentData()
            model_id = window.model_combo.currentData()
            category_id = window.category_combo.currentData()
            # Собираем код ячейки из аллеи и номера
            alley = window.alley_combo.currentText()
            cell_number = window.cell_number_input.text()
            cell_code = f"{alley}-{cell_number}" if cell_number else ""

            if not all([name, serial, brand_id, model_id, category_id]):
                QMessageBox.warning(window, "Ошибка", "Заполните все поля")
                return

            self.db.update_product(
                window.product_id,
                serial,
                name,
                quantity,
                brand_id,
                model_id,
                category_id,
                cell_code,
            )
            QMessageBox.information(window, "Успех", "Товар обновлен")
            window.close()
            self.products_window.load_products()
        except Exception as e:
            QMessageBox.critical(window, "Ошибка", f"Ошибка при обновлении: {str(e)}")

    def delete_product(self, window):
        if not window.product_id:
            QMessageBox.warning(window, "Ошибка", "Товар не выбран для удаления")
            return

        reply = QMessageBox.question(
            window,
            "Подтверждение",
            "Удалить товар?\nВнимание: все связанные заказы также будут удалены.",
        )
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_product(window.product_id)
                QMessageBox.information(
                    window, "Успех", "Товар и связанные заказы удалены"
                )
                window.close()
                self.products_window.load_products()
                self.orders_window.load_orders()
            except Exception as e:
                QMessageBox.critical(window, "Ошибка", f"Ошибка при удалении: {str(e)}")

    def save_client(self, window):
        try:
            surname = window.surname_input.text()
            name = window.name_input.text()
            patronymic = window.patronymic_input.text()
            phone = window.phone_input.text()
            address = window.address_input.text()

            if not all([surname, name]):
                QMessageBox.warning(window, "Ошибка", "Заполните обязательные поля")
                return

            self.db.add_client(surname, name, patronymic, phone, address)
            QMessageBox.information(window, "Успех", "Клиент добавлен")
            window.close()
            self.clients_window.load_clients()
        except Exception as e:
            QMessageBox.critical(window, "Ошибка", f"Ошибка при сохранении: {str(e)}")

    def update_client(self, window):
        if not window.client_id:
            QMessageBox.warning(window, "Ошибка", "Клиент не выбран для редактирования")
            return

        try:
            surname = window.surname_input.text()
            name = window.name_input.text()
            patronymic = window.patronymic_input.text()
            phone = window.phone_input.text()
            address = window.address_input.text()

            if not all([surname, name]):
                QMessageBox.warning(window, "Ошибка", "Заполните обязательные поля")
                return

            self.db.update_client(
                window.client_id, surname, name, patronymic, phone, address
            )
            QMessageBox.information(window, "Успех", "Клиент обновлен")
            window.close()
            self.clients_window.load_clients()
        except Exception as e:
            QMessageBox.critical(window, "Ошибка", f"Ошибка при обновлении: {str(e)}")

    def delete_client(self, window):
        if not window.client_id:
            QMessageBox.warning(window, "Ошибка", "Клиент не выбран для удаления")
            return

        reply = QMessageBox.question(
            window,
            "Подтверждение",
            "Удалить клиента?\nВнимание: все связанные заказы также будут удалены.",
        )
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_client(window.client_id)
                QMessageBox.information(
                    window, "Успех", "Клиент и связанные заказы удалены"
                )
                window.close()
                self.clients_window.load_clients()
                self.orders_window.load_orders()
            except Exception as e:
                QMessageBox.critical(window, "Ошибка", f"Ошибка при удалении: {str(e)}")

    def save_order(self, window):
        try:
            client_id = window.client_combo.currentData()
            order_date = window.date_input.date().toString("yyyy-MM-dd")

            if not client_id:
                QMessageBox.warning(window, "Ошибка", "Выберите клиента")
                return

            if not window.products_list:
                QMessageBox.warning(window, "Ошибка", "Добавьте товары в заказ")
                return

            # Создаем заказ и получаем его ID
            status = window.status_combo.currentText()
            order_id = self.db.add_order(
                client_id,
                order_date,
                status,
            )

            # Добавляем все товары к заказу через Order_Items и уменьшаем количество
            for product_frame in window.products_list:
                self.db.add_order_item(
                    order_id,
                    product_frame.product_id,
                    product_frame.quantity,
                )
                # Уменьшаем количество товара
                self.db.decrease_product_quantity(
                    product_frame.product_id,
                    product_frame.quantity,
                )

            QMessageBox.information(window, "Успех", "Заказ создан")
            window.close()
            self.orders_window.load_orders()
            self.products_window.load_products()  # Обновляем карточки товаров
        except Exception as e:
            QMessageBox.critical(window, "Ошибка", f"Ошибка при сохранении: {str(e)}")

    def update_order(self, window, order_id):
        try:
            client_id = window.client_combo.currentData()
            order_date = window.date_input.date().toString("yyyy-MM-dd")
            status = window.status_combo.currentText()

            if not client_id:
                QMessageBox.warning(window, "Ошибка", "Выберите клиента")
                return

            if not window.products_list:
                QMessageBox.warning(window, "Ошибка", "Добавьте товары в заказ")
                return

            # Получаем старые товары из заказа и возвращаем их количество
            old_items = self.db.get_order_products(order_id)
            for old_item in old_items:
                self.db.increase_product_quantity(
                    old_item["ProductId"],
                    old_item["Quantity"],
                )

            # Удаляем все старые товары из Order_Items
            self.db.delete_order_items(order_id)

            # Обновляем основную информацию о заказе
            self.db.update_order(
                order_id,
                client_id,
                order_date,
                status,
            )

            # Добавляем все товары к заказу через Order_Items и уменьшаем количество
            for product_frame in window.products_list:
                self.db.add_order_item(
                    order_id,
                    product_frame.product_id,
                    product_frame.quantity,
                )
                # Уменьшаем количество товара
                self.db.decrease_product_quantity(
                    product_frame.product_id,
                    product_frame.quantity,
                )

            QMessageBox.information(window, "Успех", "Заказ обновлен")
            window.close()
            self.orders_window.load_orders()
            self.products_window.load_products()  # Обновляем карточки товаров
        except Exception as e:
            QMessageBox.critical(window, "Ошибка", f"Ошибка при обновлении: {str(e)}")

    def delete_order(self, window, order_id):
        """Удаляет заказ"""
        reply = QMessageBox.question(
            window,
            "Подтверждение",
            "Удалить заказ?\nВнимание: все товары в заказе также будут удалены.",
        )
        if reply == QMessageBox.Yes:
            try:
                # Возвращаем количество товаров перед удалением
                order_items = self.db.get_order_products(order_id)
                for item in order_items:
                    self.db.increase_product_quantity(
                        item["ProductId"],
                        item["Quantity"],
                    )

                self.db.delete_order(order_id)
                QMessageBox.information(window, "Успех", "Заказ удален")
                window.close()
                self.orders_window.load_orders()
                self.products_window.load_products()  # Обновляем карточки товаров
            except Exception as e:
                QMessageBox.critical(window, "Ошибка", f"Ошибка при удалении: {str(e)}")

    def save_brand(self, window, parent_window):
        try:
            name = window.name_input.text()
            if not name:
                QMessageBox.warning(window, "Ошибка", "Введите наименование")
                return

            self.db.add_brand(name)
            QMessageBox.information(window, "Успех", "Марка добавлена")
            window.close()
            parent_window.load_data()
        except Exception as e:
            QMessageBox.critical(window, "Ошибка", f"Ошибка при сохранении: {str(e)}")

    def update_brand(self, window, parent_window):
        if not window.brand_id:
            QMessageBox.warning(window, "Ошибка", "Марка не выбрана")
            return

        try:
            name = window.name_input.text()
            if not name:
                QMessageBox.warning(window, "Ошибка", "Введите наименование")
                return

            self.db.update_brand(window.brand_id, name)
            QMessageBox.information(window, "Успех", "Марка обновлена")
            window.close()
            parent_window.load_data()
        except Exception as e:
            QMessageBox.critical(window, "Ошибка", f"Ошибка при обновлении: {str(e)}")

    def delete_brand(self, window, parent_window):
        if not window.brand_id:
            QMessageBox.warning(window, "Ошибка", "Марка не выбрана")
            return

        reply = QMessageBox.question(window, "Подтверждение", "Удалить марку?")
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_brand(window.brand_id)
                QMessageBox.information(window, "Успех", "Марка удалена")
                window.close()
                parent_window.load_data()
            except Exception as e:
                QMessageBox.critical(window, "Ошибка", f"Ошибка при удалении: {str(e)}")

    def save_model(self, window, parent_window):
        try:
            name = window.name_input.text()
            if not name:
                QMessageBox.warning(window, "Ошибка", "Введите наименование")
                return

            # Нужен brand_id, берем из родительского окна
            brand_id = parent_window.brand_combo.currentData()
            if not brand_id:
                QMessageBox.warning(window, "Ошибка", "Выберите марку в форме товара")
                return

            self.db.add_model(name, brand_id)
            QMessageBox.information(window, "Успех", "Модель добавлена")
            window.close()
            parent_window.load_data()
        except Exception as e:
            QMessageBox.critical(window, "Ошибка", f"Ошибка при сохранении: {str(e)}")

    def update_model(self, window, parent_window):
        if not window.model_id:
            QMessageBox.warning(window, "Ошибка", "Модель не выбрана")
            return

        try:
            name = window.name_input.text()
            if not name:
                QMessageBox.warning(window, "Ошибка", "Введите наименование")
                return

            brand_id = parent_window.brand_combo.currentData()
            if not brand_id:
                QMessageBox.warning(window, "Ошибка", "Выберите марку в форме товара")
                return

            self.db.update_model(window.model_id, name, brand_id)
            QMessageBox.information(window, "Успех", "Модель обновлена")
            window.close()
            parent_window.load_data()
        except Exception as e:
            QMessageBox.critical(window, "Ошибка", f"Ошибка при обновлении: {str(e)}")

    def delete_model(self, window, parent_window):
        if not window.model_id:
            QMessageBox.warning(window, "Ошибка", "Модель не выбрана")
            return

        reply = QMessageBox.question(window, "Подтверждение", "Удалить модель?")
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_model(window.model_id)
                QMessageBox.information(window, "Успех", "Модель удалена")
                window.close()
                parent_window.load_data()
            except Exception as e:
                QMessageBox.critical(window, "Ошибка", f"Ошибка при удалении: {str(e)}")

    def save_category(self, window, parent_window):
        try:
            name = window.name_input.text()
            if not name:
                QMessageBox.warning(window, "Ошибка", "Введите наименование")
                return

            self.db.add_category(name)
            QMessageBox.information(window, "Успех", "Категория добавлена")
            window.close()
            parent_window.load_data()
        except Exception as e:
            QMessageBox.critical(window, "Ошибка", f"Ошибка при сохранении: {str(e)}")

    def update_category(self, window, parent_window):
        if not window.category_id:
            QMessageBox.warning(window, "Ошибка", "Категория не выбрана")
            return

        try:
            name = window.name_input.text()
            if not name:
                QMessageBox.warning(window, "Ошибка", "Введите наименование")
                return

            self.db.update_category(window.category_id, name)
            QMessageBox.information(window, "Успех", "Категория обновлена")
            window.close()
            parent_window.load_data()
        except Exception as e:
            QMessageBox.critical(window, "Ошибка", f"Ошибка при обновлении: {str(e)}")

    def delete_category(self, window, parent_window):
        if not window.category_id:
            QMessageBox.warning(window, "Ошибка", "Категория не выбрана")
            return

        reply = QMessageBox.question(window, "Подтверждение", "Удалить категорию?")
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_category(window.category_id)
                QMessageBox.information(window, "Успех", "Категория удалена")
                window.close()
                parent_window.load_data()
            except Exception as e:
                QMessageBox.critical(window, "Ошибка", f"Ошибка при удалении: {str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    controller = AppController()
    controller.stacked_widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
