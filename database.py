import psycopg2
from typing import List, Dict, Optional


class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """Подключение к базе данных PostgreSQL"""
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="project",
                user="postgres",
                password="123456",
                port="5432",
            )
            self.connection.autocommit = True
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")

    # Методы для работы с марками
    def get_brands(self) -> List[Dict]:
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute("SELECT id, name FROM carbrand ORDER BY name")
            return [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        else:
            cursor.execute("SELECT id, name FROM carbrand ORDER BY name")
            rows = cursor.fetchall()
            return [{"id": row[0], "name": row[1]} for row in rows]

    def add_brand(self, name: str) -> int:
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                "INSERT INTO carbrand (name) VALUES (%s) RETURNING id", (name,)
            )
            return cursor.fetchone()[0]
        else:
            cursor.execute("INSERT INTO carbrand (name) VALUES (?)", (name,))
            return cursor.lastrowid

    def update_brand(self, brand_id: int, name: str):
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                "UPDATE carbrand SET name = %s WHERE id = %s", (name, brand_id)
            )
        else:
            cursor.execute(
                "UPDATE carbrand SET name = ? WHERE id = ?", (name, brand_id)
            )

    def delete_brand(self, brand_id: int):
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute("DELETE FROM carbrand WHERE id = %s", (brand_id,))
        else:
            cursor.execute("DELETE FROM carbrand WHERE id = ?", (brand_id,))

    # Методы для работы с категориями
    def get_categories(self) -> List[Dict]:
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute("SELECT id, name FROM category ORDER BY name")
            return [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        else:
            cursor.execute("SELECT id, name FROM category ORDER BY name")
            rows = cursor.fetchall()
            return [{"id": row[0], "name": row[1]} for row in rows]

    def add_category(self, name: str) -> int:
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                "INSERT INTO category (name) VALUES (%s) RETURNING id", (name,)
            )
            return cursor.fetchone()[0]
        else:
            cursor.execute("INSERT INTO category (name) VALUES (?)", (name,))
            return cursor.lastrowid

    def update_category(self, category_id: int, name: str):
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                "UPDATE category SET name = %s WHERE id = %s", (name, category_id)
            )
        else:
            cursor.execute(
                "UPDATE category SET name = ? WHERE id = ?", (name, category_id)
            )

    def delete_category(self, category_id: int):
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute("DELETE FROM category WHERE id = %s", (category_id,))
        else:
            cursor.execute("DELETE FROM category WHERE id = ?", (category_id,))

    # Методы для работы с моделями
    def get_models(self, brand_id: Optional[int] = None) -> List[Dict]:
        cursor = self.connection.cursor()
        if brand_id:
            if isinstance(self.connection, psycopg2.extensions.connection):
                cursor.execute(
                    "SELECT id, name, brand_id FROM carmodel WHERE brand_id = %s ORDER BY name",
                    (brand_id,),
                )
            else:
                cursor.execute(
                    "SELECT id, name, brand_id FROM carmodel WHERE brand_id = ? ORDER BY name",
                    (brand_id,),
                )
        else:
            cursor.execute("SELECT id, name, brand_id FROM carmodel ORDER BY name")

        if isinstance(self.connection, psycopg2.extensions.connection):
            return [
                {"id": row[0], "name": row[1], "brand_id": row[2]}
                for row in cursor.fetchall()
            ]
        else:
            rows = cursor.fetchall()
            return [{"id": row[0], "name": row[1], "brand_id": row[2]} for row in rows]

    def add_model(self, name: str, brand_id: int) -> int:
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                "INSERT INTO carmodel (name, brand_id) VALUES (%s, %s) RETURNING id",
                (name, brand_id),
            )
            return cursor.fetchone()[0]
        else:
            cursor.execute(
                "INSERT INTO carmodel (name, brand_id) VALUES (?, ?)", (name, brand_id)
            )
            return cursor.lastrowid

    def update_model(self, model_id: int, name: str, brand_id: int):
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                "UPDATE carmodel SET name = %s, brand_id = %s WHERE id = %s",
                (name, brand_id, model_id),
            )
        else:
            cursor.execute(
                "UPDATE carmodel SET name = ?, brand_id = ? WHERE id = ?",
                (name, brand_id, model_id),
            )

    def delete_model(self, model_id: int):
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute("DELETE FROM carmodel WHERE id = %s", (model_id,))
        else:
            cursor.execute("DELETE FROM carmodel WHERE id = ?", (model_id,))

    # Методы для работы с товарами
    def get_products(self, search: str = "") -> List[Dict]:
        cursor = self.connection.cursor()
        if search:
            if isinstance(self.connection, psycopg2.extensions.connection):
                cursor.execute(
                    """
                    SELECT p."Id", p."SerialNumber", p."Name", p."Quantity", 
                           p."brand_id", p."model_id", p."category_id",
                           b.name as brand_name, m.name as model_name, c.name as category_name
                    FROM "Product" p
                    LEFT JOIN carbrand b ON p."brand_id" = b.id
                    LEFT JOIN carmodel m ON p."model_id" = m.id
                    LEFT JOIN category c ON p."category_id" = c.id
                    WHERE p."Name" ILIKE %s OR p."SerialNumber" ILIKE %s
                    ORDER BY p."Name"
                """,
                    (f"%{search}%", f"%{search}%"),
                )
            else:
                cursor.execute(
                    """
                    SELECT p.id, p.SerialNumber, p.Name, p.Quantity, 
                           p.brand_id, p.model_id, p.category_id,
                           b.name as brand_name, m.name as model_name, c.name as category_name
                    FROM Product p
                    LEFT JOIN carbrand b ON p.brand_id = b.id
                    LEFT JOIN carmodel m ON p.model_id = m.id
                    LEFT JOIN category c ON p.category_id = c.id
                    WHERE p.Name LIKE ? OR p.SerialNumber LIKE ?
                    ORDER BY p.Name
                """,
                    (f"%{search}%", f"%{search}%"),
                )
        else:
            if isinstance(self.connection, psycopg2.extensions.connection):
                cursor.execute(
                    """
                    SELECT p."Id", p."SerialNumber", p."Name", p."Quantity", 
                           p."brand_id", p."model_id", p."category_id",
                           b.name as brand_name, m.name as model_name, c.name as category_name
                    FROM "Product" p
                    LEFT JOIN carbrand b ON p."brand_id" = b.id
                    LEFT JOIN carmodel m ON p."model_id" = m.id
                    LEFT JOIN category c ON p."category_id" = c.id
                    ORDER BY p."Name"
                """
                )
            else:
                cursor.execute(
                    """
                    SELECT p.id, p.SerialNumber, p.Name, p.Quantity, 
                           p.brand_id, p.model_id, p.category_id,
                           b.name as brand_name, m.name as model_name, c.name as category_name
                    FROM Product p
                    LEFT JOIN carbrand b ON p.brand_id = b.id
                    LEFT JOIN carmodel m ON p.model_id = m.id
                    LEFT JOIN category c ON p.category_id = c.id
                    ORDER BY p.Name
                """
                )

        if isinstance(self.connection, psycopg2.extensions.connection):
            rows = cursor.fetchall()
            return [
                {
                    "Id": row[0],
                    "SerialNumber": row[1],
                    "Name": row[2],
                    "Quantity": row[3],
                    "brand_id": row[4],
                    "model_id": row[5],
                    "category_id": row[6],
                    "brand_name": row[7],
                    "model_name": row[8],
                    "category_name": row[9],
                }
                for row in rows
            ]
        else:
            rows = cursor.fetchall()
            return [
                {
                    "Id": row[0],
                    "SerialNumber": row[1],
                    "Name": row[2],
                    "Quantity": row[3],
                    "brand_id": row[4],
                    "model_id": row[5],
                    "category_id": row[6],
                    "brand_name": row[7],
                    "model_name": row[8],
                    "category_name": row[9],
                }
                for row in rows
            ]

    def add_product(
        self,
        serial_number: str,
        name: str,
        quantity: int,
        brand_id: int,
        model_id: int,
        category_id: int,
        cell_code: str = "",
    ) -> int:
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                """
                INSERT INTO "Product" ("SerialNumber", "Name", "Quantity", "brand_id", "model_id", "category_id")
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING "Id"
            """,
                (serial_number, name, quantity, brand_id, model_id, category_id),
            )
            product_id = cursor.fetchone()[0]
        else:
            cursor.execute(
                """
                INSERT INTO Product (SerialNumber, Name, Quantity, brand_id, model_id, category_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (serial_number, name, quantity, brand_id, model_id, category_id),
            )
            product_id = cursor.lastrowid

        if cell_code:
            if isinstance(self.connection, psycopg2.extensions.connection):
                # Пробуем с кавычками, если не работает - без кавычек
                try:
                    cursor.execute(
                        """
                        INSERT INTO public."StorageCell" ("CellCode", "ProductId", "Quantity")
                        VALUES (%s, %s, %s)
                    """,
                        (cell_code, product_id, quantity),
                    )
                except Exception:
                    cursor.execute(
                        """
                        INSERT INTO public.storagecell (cellcode, productid, quantity)
                        VALUES (%s, %s, %s)
                    """,
                        (cell_code, product_id, quantity),
                    )
            else:
                cursor.execute(
                    """
                    INSERT INTO StorageCell (CellCode, ProductId, Quantity)
                    VALUES (?, ?, ?)
                """,
                    (cell_code, product_id, quantity),
                )

        return product_id

    def update_product(
        self,
        product_id: int,
        serial_number: str,
        name: str,
        quantity: int,
        brand_id: int,
        model_id: int,
        category_id: int,
        cell_code: str = "",
    ):
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                """
                UPDATE "Product" SET "SerialNumber" = %s, "Name" = %s, "Quantity" = %s,
                "brand_id" = %s, "model_id" = %s, "category_id" = %s WHERE "Id" = %s
            """,
                (
                    serial_number,
                    name,
                    quantity,
                    brand_id,
                    model_id,
                    category_id,
                    product_id,
                ),
            )
        else:
            cursor.execute(
                """
                UPDATE Product SET SerialNumber = ?, Name = ?, Quantity = ?,
                brand_id = ?, model_id = ?, category_id = ? WHERE id = ?
            """,
                (
                    serial_number,
                    name,
                    quantity,
                    brand_id,
                    model_id,
                    category_id,
                    product_id,
                ),
            )

        # Обновляем или создаем запись в StorageCell
        # ВАЖНО: Количество в StorageCell всегда должно равняться количеству в Product
        if cell_code:
            # Если ячейка указана, обновляем/создаем запись с новым количеством
            if isinstance(self.connection, psycopg2.extensions.connection):
                # Пробуем с кавычками, если не работает - без кавычек
                try:
                    # Проверяем, существует ли запись
                    cursor.execute(
                        """
                        SELECT "Id" FROM public."StorageCell"
                        WHERE "ProductId" = %s
                        LIMIT 1
                    """,
                        (product_id,),
                    )
                    exists = cursor.fetchone()
                    if exists:
                        # Обновляем существующую запись (количество синхронизируется с Product)
                        cursor.execute(
                            """
                            UPDATE public."StorageCell" SET "CellCode" = %s, "Quantity" = %s
                            WHERE "ProductId" = %s
                        """,
                            (cell_code, quantity, product_id),
                        )
                    else:
                        # Создаем новую запись (количество равно количеству в Product)
                        cursor.execute(
                            """
                            INSERT INTO public."StorageCell" ("CellCode", "ProductId", "Quantity")
                            VALUES (%s, %s, %s)
                        """,
                            (cell_code, product_id, quantity),
                        )
                except Exception:
                    # Проверяем, существует ли запись (без кавычек)
                    cursor.execute(
                        """
                        SELECT id FROM public.storagecell
                        WHERE productid = %s
                        LIMIT 1
                    """,
                        (product_id,),
                    )
                    exists = cursor.fetchone()
                    if exists:
                        # Обновляем существующую запись (количество синхронизируется с Product)
                        cursor.execute(
                            """
                            UPDATE public.storagecell SET cellcode = %s, quantity = %s
                            WHERE productid = %s
                        """,
                            (cell_code, quantity, product_id),
                        )
                    else:
                        # Создаем новую запись (количество равно количеству в Product)
                        cursor.execute(
                            """
                            INSERT INTO public.storagecell (cellcode, productid, quantity)
                            VALUES (%s, %s, %s)
                        """,
                            (cell_code, product_id, quantity),
                        )
            else:
                # Проверяем, существует ли запись
                cursor.execute(
                    """
                    SELECT Id FROM StorageCell
                    WHERE ProductId = ?
                    LIMIT 1
                """,
                    (product_id,),
                )
                exists = cursor.fetchone()
                if exists:
                    # Обновляем существующую запись (количество синхронизируется с Product)
                    cursor.execute(
                        """
                        UPDATE StorageCell SET CellCode = ?, Quantity = ?
                        WHERE ProductId = ?
                    """,
                        (cell_code, quantity, product_id),
                    )
                else:
                    # Создаем новую запись (количество равно количеству в Product)
                    cursor.execute(
                        """
                        INSERT INTO StorageCell (CellCode, ProductId, Quantity)
                        VALUES (?, ?, ?)
                    """,
                        (cell_code, product_id, quantity),
                    )
        else:
            # Если ячейка не указана, но запись существует, синхронизируем количество с Product
            if isinstance(self.connection, psycopg2.extensions.connection):
                try:
                    cursor.execute(
                        """
                        UPDATE public."StorageCell" SET "Quantity" = %s
                        WHERE "ProductId" = %s
                    """,
                        (quantity, product_id),
                    )
                except Exception:
                    try:
                        cursor.execute(
                            """
                            UPDATE public.storagecell SET quantity = %s
                            WHERE productid = %s
                        """,
                            (quantity, product_id),
                        )
                    except Exception:
                        pass  # Если записи нет, ничего не делаем
            else:
                try:
                    cursor.execute(
                        """
                        UPDATE StorageCell SET Quantity = ?
                        WHERE ProductId = ?
                    """,
                        (quantity, product_id),
                    )
                except Exception:
                    pass  # Если записи нет, ничего не делаем

    def get_product_cell_code(self, product_id: int) -> str:
        """Получает код ячейки для товара"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            try:
                cursor.execute(
                    """
                    SELECT "CellCode" FROM public."StorageCell"
                    WHERE "ProductId" = %s
                    LIMIT 1
                    """,
                    (product_id,),
                )
            except Exception:
                cursor.execute(
                    """
                    SELECT cellcode FROM public.storagecell
                    WHERE productid = %s
                    LIMIT 1
                    """,
                    (product_id,),
                )
        else:
            cursor.execute(
                """
                SELECT CellCode FROM StorageCell
                WHERE ProductId = ?
                LIMIT 1
                """,
                (product_id,),
            )
        row = cursor.fetchone()
        return row[0] if row and row[0] else ""

    def delete_orders_by_product(self, product_id: int):
        """Удаляет все заказы, связанные с товаром"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            # Получаем ID заказов, содержащих этот товар
            cursor.execute(
                'SELECT DISTINCT "order_id" FROM "order_items" WHERE "product_id" = %s',
                (product_id,),
            )
            order_ids = [row[0] for row in cursor.fetchall()]
            # Удаляем товары из order_items
            cursor.execute(
                'DELETE FROM "order_items" WHERE "product_id" = %s', (product_id,)
            )
            # Удаляем заказы, если они пустые (не содержат других товаров)
            if order_ids:
                # Проверяем, есть ли в заказах другие товары
                for order_id in order_ids:
                    cursor.execute(
                        'SELECT COUNT(*) FROM "order_items" WHERE "order_id" = %s',
                        (order_id,),
                    )
                    count = cursor.fetchone()[0]
                    if count == 0:
                        cursor.execute(
                            'DELETE FROM "Order" WHERE "Id" = %s', (order_id,)
                        )
        else:
            cursor.execute(
                'SELECT DISTINCT order_id FROM "order_items" WHERE product_id = ?',
                (product_id,),
            )
            order_ids = [row[0] for row in cursor.fetchall()]
            cursor.execute(
                'DELETE FROM "order_items" WHERE product_id = ?', (product_id,)
            )
            # Удаляем заказы, если они пустые
            for order_id in order_ids:
                cursor.execute(
                    'SELECT COUNT(*) FROM "order_items" WHERE order_id = ?',
                    (order_id,),
                )
                count = cursor.fetchone()[0]
                if count == 0:
                    cursor.execute('DELETE FROM "Order" WHERE Id = ?', (order_id,))

    def delete_orders_by_client(self, client_id: int):
        """Удаляет все заказы, связанные с клиентом"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            # Получаем ID заказов клиента
            cursor.execute(
                'SELECT "Id" FROM "Order" WHERE "ClientId" = %s', (client_id,)
            )
            order_ids = [row[0] for row in cursor.fetchall()]
            # Удаляем товары из order_items
            if order_ids:
                # Используем правильный синтаксис для PostgreSQL
                placeholders = ",".join(["%s"] * len(order_ids))
                cursor.execute(
                    f'DELETE FROM "order_items" WHERE "order_id" IN ({placeholders})',
                    order_ids,
                )
            # Удаляем заказы
            cursor.execute('DELETE FROM "Order" WHERE "ClientId" = %s', (client_id,))
        else:
            cursor.execute('SELECT Id FROM "Order" WHERE ClientId = ?', (client_id,))
            order_ids = [row[0] for row in cursor.fetchall()]
            if order_ids:
                placeholders = ",".join("?" * len(order_ids))
                cursor.execute(
                    f'DELETE FROM "order_items" WHERE order_id IN ({placeholders})',
                    order_ids,
                )
            cursor.execute('DELETE FROM "Order" WHERE ClientId = ?', (client_id,))

    def delete_product(self, product_id: int):
        cursor = self.connection.cursor()
        # Сначала удаляем связанные заказы (каскадное удаление)
        self.delete_orders_by_product(product_id)
        # Удаляем запись из StorageCell
        if isinstance(self.connection, psycopg2.extensions.connection):
            try:
                cursor.execute(
                    'DELETE FROM public."StorageCell" WHERE "ProductId" = %s',
                    (product_id,),
                )
            except Exception:
                cursor.execute(
                    "DELETE FROM public.storagecell WHERE productid = %s",
                    (product_id,),
                )
        else:
            cursor.execute("DELETE FROM StorageCell WHERE ProductId = ?", (product_id,))
        # Затем удаляем сам товар
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute('DELETE FROM "Product" WHERE "Id" = %s', (product_id,))
        else:
            cursor.execute("DELETE FROM Product WHERE id = ?", (product_id,))

    # Методы для работы с клиентами
    def get_clients(self) -> List[Dict]:
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                'SELECT "Id", surname, name, patronymic, "Phone", "Address" FROM "Client" ORDER BY "Id" ASC'
            )
            rows = cursor.fetchall()
            return [
                {
                    "Id": row[0],
                    "surname": row[1],
                    "name": row[2],
                    "patronymic": row[3],
                    "Phone": row[4],
                    "Address": row[5],
                }
                for row in rows
            ]
        else:
            cursor.execute(
                "SELECT Id, surname, name, patronymic, Phone, Address FROM Client ORDER BY Id ASC"
            )
            rows = cursor.fetchall()
            return [
                {
                    "Id": row[0],
                    "surname": row[1],
                    "name": row[2],
                    "patronymic": row[3],
                    "Phone": row[4],
                    "Address": row[5],
                }
                for row in rows
            ]

    def add_client(
        self, surname: str, name: str, patronymic: str, phone: str, address: str
    ) -> int:
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                'INSERT INTO "Client" (surname, name, patronymic, "Phone", "Address") VALUES (%s, %s, %s, %s, %s) RETURNING "Id"',
                (surname, name, patronymic, phone, address),
            )
            return cursor.fetchone()[0]
        else:
            cursor.execute(
                "INSERT INTO Client (surname, name, patronymic, Phone, Address) VALUES (?, ?, ?, ?, ?)",
                (surname, name, patronymic, phone, address),
            )
            return cursor.lastrowid

    def update_client(
        self,
        client_id: int,
        surname: str,
        name: str,
        patronymic: str,
        phone: str,
        address: str,
    ):
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                'UPDATE "Client" SET surname = %s, name = %s, patronymic = %s, "Phone" = %s, "Address" = %s WHERE "Id" = %s',
                (surname, name, patronymic, phone, address, client_id),
            )
        else:
            cursor.execute(
                "UPDATE Client SET surname = ?, name = ?, patronymic = ?, Phone = ?, Address = ? WHERE Id = ?",
                (surname, name, patronymic, phone, address, client_id),
            )

    def delete_client(self, client_id: int):
        cursor = self.connection.cursor()
        # Сначала удаляем связанные заказы (каскадное удаление)
        self.delete_orders_by_client(client_id)
        # Затем удаляем самого клиента
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute('DELETE FROM "Client" WHERE "Id" = %s', (client_id,))
        else:
            cursor.execute("DELETE FROM Client WHERE Id = ?", (client_id,))

    # Методы для работы с заказами
    def get_orders(self) -> List[Dict]:
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                """
                SELECT o."Id", o."ClientId", o."OrderDate", o."Status",
                       oi."product_id" as "ProductId", oi."quantity" as "Quantity",
                       p."Name" as product_name, 
                       c.surname || ' ' || c.name || ' ' || c.patronymic as client_name
                FROM "Order" o
                LEFT JOIN "order_items" oi ON o."Id" = oi."order_id"
                LEFT JOIN "Product" p ON oi."product_id" = p."Id"
                LEFT JOIN "Client" c ON o."ClientId" = c."Id"
                ORDER BY o."OrderDate" ASC, o."Id" ASC
            """
            )
            rows = cursor.fetchall()
            return [
                {
                    "Id": row[0],
                    "ClientId": row[1],
                    "OrderDate": row[2],
                    "Status": row[3],
                    "ProductId": row[4],
                    "Quantity": row[5],
                    "product_name": row[6],
                    "client_name": row[7],
                }
                for row in rows
            ]
        else:
            cursor.execute(
                """
                SELECT o.Id, o.ClientId, o.OrderDate, o.Status,
                       oi.product_id as ProductId, oi.quantity as Quantity,
                       p.Name as product_name,
                       c.surname || ' ' || c.name || ' ' || c.patronymic as client_name
                FROM "Order" o
                LEFT JOIN "order_items" oi ON o.Id = oi.order_id
                LEFT JOIN Product p ON oi.product_id = p.id
                LEFT JOIN Client c ON o.ClientId = c.Id
                ORDER BY o.OrderDate ASC, o.Id ASC
            """
            )
            rows = cursor.fetchall()
            return [
                {
                    "Id": row[0],
                    "ClientId": row[1],
                    "OrderDate": row[2],
                    "Status": row[3],
                    "ProductId": row[4],
                    "Quantity": row[5],
                    "product_name": row[6],
                    "client_name": row[7],
                }
                for row in rows
            ]

    def add_order(
        self,
        client_id: int,
        order_date: str,
        status: str,
    ) -> int:
        """Создает новый заказ и возвращает его ID"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                'INSERT INTO "Order" ("ClientId", "OrderDate", "Status") VALUES (%s, %s, %s) RETURNING "Id"',
                (client_id, order_date, status),
            )
            return cursor.fetchone()[0]
        else:
            cursor.execute(
                'INSERT INTO "Order" (ClientId, OrderDate, Status) VALUES (?, ?, ?)',
                (client_id, order_date, status),
            )
            return cursor.lastrowid

    def update_order(
        self,
        order_id: int,
        client_id: int,
        order_date: str,
        status: str,
    ):
        """Обновляет основную информацию о заказе"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                'UPDATE "Order" SET "ClientId" = %s, "OrderDate" = %s, "Status" = %s WHERE "Id" = %s',
                (client_id, order_date, status, order_id),
            )
        else:
            cursor.execute(
                'UPDATE "Order" SET ClientId = ?, OrderDate = ?, Status = ? WHERE Id = ?',
                (client_id, order_date, status, order_id),
            )

    def add_order_item(
        self,
        order_id: int,
        product_id: int,
        quantity: int,
    ):
        """Добавляет товар к существующему заказу в таблицу order_items"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                'INSERT INTO "order_items" ("order_id", "product_id", "quantity") VALUES (%s, %s, %s)',
                (order_id, product_id, quantity),
            )
        else:
            cursor.execute(
                'INSERT INTO "order_items" (order_id, product_id, quantity) VALUES (?, ?, ?)',
                (order_id, product_id, quantity),
            )

    def delete_order_items(self, order_id: int):
        """Удаляет все товары из заказа"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                'DELETE FROM "order_items" WHERE "order_id" = %s', (order_id,)
            )
        else:
            cursor.execute('DELETE FROM "order_items" WHERE order_id = ?', (order_id,))

    def delete_order(self, order_id: int):
        """Удаляет заказ и все его товары"""
        cursor = self.connection.cursor()
        # Сначала удаляем товары из order_items
        self.delete_order_items(order_id)
        # Затем удаляем сам заказ
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute('DELETE FROM "Order" WHERE "Id" = %s', (order_id,))
        else:
            cursor.execute('DELETE FROM "Order" WHERE Id = ?', (order_id,))

    def get_order_products(self, order_id: int) -> List[Dict]:
        """Получить все товары в заказе из таблицы order_items"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor.execute(
                """
                SELECT oi."product_id" as "ProductId", oi."quantity" as "Quantity", p."Name" as product_name
                FROM "order_items" oi
                LEFT JOIN "Product" p ON oi."product_id" = p."Id"
                WHERE oi."order_id" = %s
            """,
                (order_id,),
            )
            rows = cursor.fetchall()
            return [
                {"ProductId": row[0], "Quantity": row[1], "product_name": row[2]}
                for row in rows
            ]
        else:
            cursor.execute(
                """
                SELECT oi.product_id as ProductId, oi.quantity as Quantity, p.Name as product_name
                FROM "order_items" oi
                LEFT JOIN Product p ON oi.product_id = p.id
                WHERE oi.order_id = ?
            """,
                (order_id,),
            )
            rows = cursor.fetchall()
            return [
                {"ProductId": row[0], "Quantity": row[1], "product_name": row[2]}
                for row in rows
            ]

    def decrease_product_quantity(self, product_id: int, quantity: int):
        """Уменьшает количество товара на складе (и в Product, и в StorageCell)"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            # Уменьшаем количество в Product
            cursor.execute(
                'UPDATE "Product" SET "Quantity" = "Quantity" - %s WHERE "Id" = %s',
                (quantity, product_id),
            )
            # Уменьшаем количество в StorageCell, если запись существует
            try:
                cursor.execute(
                    """
                    UPDATE public."StorageCell" SET "Quantity" = "Quantity" - %s
                    WHERE "ProductId" = %s
                    """,
                    (quantity, product_id),
                )
            except Exception:
                try:
                    cursor.execute(
                        """
                        UPDATE public.storagecell SET quantity = quantity - %s
                        WHERE productid = %s
                        """,
                        (quantity, product_id),
                    )
                except Exception:
                    pass  # Если записи нет, просто пропускаем
        else:
            # Уменьшаем количество в Product
            cursor.execute(
                "UPDATE Product SET Quantity = Quantity - ? WHERE id = ?",
                (quantity, product_id),
            )
            # Уменьшаем количество в StorageCell, если запись существует
            try:
                cursor.execute(
                    """
                    UPDATE StorageCell SET Quantity = Quantity - ?
                    WHERE ProductId = ?
                    """,
                    (quantity, product_id),
                )
            except Exception:
                pass  # Если записи нет, просто пропускаем

    def increase_product_quantity(self, product_id: int, quantity: int):
        """Увеличивает количество товара на складе (и в Product, и в StorageCell)"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            # Увеличиваем количество в Product
            cursor.execute(
                'UPDATE "Product" SET "Quantity" = "Quantity" + %s WHERE "Id" = %s',
                (quantity, product_id),
            )
            # Увеличиваем количество в StorageCell, если запись существует
            try:
                cursor.execute(
                    """
                    UPDATE public."StorageCell" SET "Quantity" = "Quantity" + %s
                    WHERE "ProductId" = %s
                    """,
                    (quantity, product_id),
                )
            except Exception:
                try:
                    cursor.execute(
                        """
                        UPDATE public.storagecell SET quantity = quantity + %s
                        WHERE productid = %s
                        """,
                        (quantity, product_id),
                    )
                except Exception:
                    pass  # Если записи нет, просто пропускаем
        else:
            # Увеличиваем количество в Product
            cursor.execute(
                "UPDATE Product SET Quantity = Quantity + ? WHERE id = ?",
                (quantity, product_id),
            )
            # Увеличиваем количество в StorageCell, если запись существует
            try:
                cursor.execute(
                    """
                    UPDATE StorageCell SET Quantity = Quantity + ?
                    WHERE ProductId = ?
                    """,
                    (quantity, product_id),
                )
            except Exception:
                pass  # Если записи нет, просто пропускаем

    def sync_storage_quantities(self):
        """Синхронизирует количество в StorageCell с количеством в Product для всех товаров"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            try:
                # Синхронизируем количество для всех товаров, у которых есть запись в StorageCell
                cursor.execute(
                    """
                    UPDATE public."StorageCell" sc
                    SET "Quantity" = p."Quantity"
                    FROM "Product" p
                    WHERE sc."ProductId" = p."Id"
                    """
                )
            except Exception:
                try:
                    cursor.execute(
                        """
                        UPDATE public.storagecell sc
                        SET quantity = p."Quantity"
                        FROM "Product" p
                        WHERE sc.productid = p."Id"
                        """
                    )
                except Exception:
                    pass
        else:
            cursor.execute(
                """
                UPDATE StorageCell
                SET Quantity = (
                    SELECT Quantity FROM Product
                    WHERE Product.id = StorageCell.ProductId
                )
                WHERE EXISTS (
                    SELECT 1 FROM Product
                    WHERE Product.id = StorageCell.ProductId
                )
                """
            )

    def get_warehouse_alleys(self) -> List[str]:
        """Получает список уникальных аллей (первая буква из CellCode)"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            # Пробуем с кавычками (если таблица создана с кавычками)
            try:
                cursor.execute(
                    """
                    SELECT DISTINCT UPPER(SUBSTRING("CellCode" FROM 1 FOR 1)) as alley
                    FROM public."StorageCell"
                    WHERE "CellCode" IS NOT NULL AND "CellCode" != ''
                    ORDER BY alley
                    """
                )
            except Exception:
                # Если таблица создана без кавычек, используем нижний регистр
                cursor.execute(
                    """
                    SELECT DISTINCT UPPER(SUBSTRING(cellcode FROM 1 FOR 1)) as alley
                    FROM public.storagecell
                    WHERE cellcode IS NOT NULL AND cellcode != ''
                    ORDER BY alley
                    """
                )
        else:
            cursor.execute(
                """
                SELECT DISTINCT UPPER(SUBSTR(CellCode, 1, 1)) as alley
                FROM StorageCell
                WHERE CellCode IS NOT NULL AND CellCode != ''
                ORDER BY alley
                """
            )
        rows = cursor.fetchall()
        return [row[0] for row in rows if row[0]]

    def get_products_by_alley(self, alley: str) -> List[Dict]:
        """Получает все товары на указанной аллее"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            # Пробуем с кавычками (если таблица создана с кавычками)
            try:
                cursor.execute(
                    """
                    SELECT sc."Id" as cell_id, sc."CellCode", sc."Quantity" as cell_quantity,
                           p."Id" as product_id, p."Name", p."SerialNumber", p."Quantity" as product_quantity,
                           b.name as brand_name, m.name as model_name, c.name as category_name
                    FROM public."StorageCell" sc
                    INNER JOIN "Product" p ON sc."ProductId" = p."Id"
                    LEFT JOIN carbrand b ON p."brand_id" = b.id
                    LEFT JOIN carmodel m ON p."model_id" = m.id
                    LEFT JOIN category c ON p."category_id" = c.id
                    WHERE UPPER(SUBSTRING(sc."CellCode" FROM 1 FOR 1)) = %s
                    ORDER BY sc."CellCode"
                    """,
                    (alley.upper(),),
                )
            except Exception:
                # Если таблица создана без кавычек, используем нижний регистр
                cursor.execute(
                    """
                    SELECT sc.id as cell_id, sc.cellcode, sc.quantity as cell_quantity,
                           p."Id" as product_id, p."Name", p."SerialNumber", p."Quantity" as product_quantity,
                           b.name as brand_name, m.name as model_name, c.name as category_name
                    FROM public.storagecell sc
                    INNER JOIN "Product" p ON sc.productid = p."Id"
                    LEFT JOIN carbrand b ON p."brand_id" = b.id
                    LEFT JOIN carmodel m ON p."model_id" = m.id
                    LEFT JOIN category c ON p."category_id" = c.id
                    WHERE UPPER(SUBSTRING(sc.cellcode FROM 1 FOR 1)) = %s
                    ORDER BY sc.cellcode
                    """,
                    (alley.upper(),),
                )
        else:
            cursor.execute(
                """
                SELECT sc.Id as cell_id, sc.CellCode, sc.Quantity as cell_quantity,
                       p.Id as product_id, p.Name, p.SerialNumber, p.Quantity as product_quantity,
                       b.name as brand_name, m.name as model_name, c.name as category_name
                FROM StorageCell sc
                INNER JOIN Product p ON sc.ProductId = p.id
                LEFT JOIN carbrand b ON p.brand_id = b.id
                LEFT JOIN carmodel m ON p.model_id = m.id
                LEFT JOIN category c ON p.category_id = c.id
                WHERE UPPER(SUBSTR(sc.CellCode, 1, 1)) = ?
                ORDER BY sc.CellCode
                """,
                (alley.upper(),),
            )
        rows = cursor.fetchall()
        return [
            {
                "cell_id": row[0],
                "CellCode": row[1],
                "cell_quantity": row[2],
                "product_id": row[3],
                "Name": row[4],
                "SerialNumber": row[5],
                "product_quantity": row[6],
                "brand_name": row[7],
                "model_name": row[8],
                "category_name": row[9],
            }
            for row in rows
        ]

    def get_order_statuses(self) -> List[str]:
        """Получает список статусов заказов из базы данных"""
        cursor = self.connection.cursor()
        if isinstance(self.connection, psycopg2.extensions.connection):
            # Для PostgreSQL получаем значения из ENUM типа
            try:
                cursor.execute(
                    """
                    SELECT enumlabel 
                    FROM pg_enum 
                    WHERE enumtypid = (
                        SELECT oid 
                        FROM pg_type 
                        WHERE typname = 'order_status_enum'
                    )
                    ORDER BY enumsortorder
                    """
                )
                rows = cursor.fetchall()
                if rows:
                    return [row[0] for row in rows]
            except Exception:
                # Если ENUM не найден, возвращаем значения по умолчанию
                pass
            # Если ENUM не найден, возвращаем значения по умолчанию
            return ["Создан", "Оформлен", "Завершен"]
        else:
            # Для SQLite возвращаем значения по умолчанию
            return ["Создан", "Оформлен", "Завершен"]

    def close(self):
        if self.connection:
            self.connection.close()
