import psycopg2
from tabulate import tabulate
from mimesis import Person, Datetime, Finance, Text, Address
from mimesis.enums import Gender
import random
from datetime import datetime, timedelta

# Данные для подключения
DB_NAME = "test"
DB_USER = "postgres"
DB_PASSWORD = "12345678"
DB_HOST = "localhost"

# Инициализация генераторов данных
person = Person('ru')
dt = Datetime()
finance = Finance()
text = Text()
address = Address()


def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        print("✅ Успешное подключение к БД")
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return None


def show_employees():
    conn = connect_to_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        # Запрашиваем параметры фильтрации и сортировки
        print("\nПараметры отображения списка сотрудников:")

        # Фильтрация
        print("\nФильтрация (оставьте пустым, если не нужно):")
        position_filter = input("Должность (например 'Разработчик'): ").strip()
        level_filter = input("Уровень (например 'Junior'): ").strip()
        salary_min = input("Минимальная зарплата: ").strip()
        salary_max = input("Максимальная зарплата: ").strip()

        # Сортировка
        print("\nСортировка:")
        print("Доступные поля: id, first_name, last_name, position, level, hire_date, salary")
        sort_field = input("Поле для сортировки (по умолчанию id): ").strip() or "id"
        sort_order = input("Порядок (ASC/DESC, по умолчанию ASC): ").strip().upper() or "ASC"

        # Формируем SQL запрос
        sql = """
            SELECT e.id, e.first_name, e.last_name, e.middle_name, 
                   p.title as position, p.level, e.hire_date, e.salary, 
                   m.first_name || ' ' || m.last_name as manager
            FROM employees e
            LEFT JOIN positions p ON e.position_id = p.id
            LEFT JOIN employees m ON e.manager_id = m.id
        """

        # Добавляем условия фильтрации
        conditions = []
        params = []

        if position_filter:
            conditions.append("p.title = %s")
            params.append(position_filter)

        if level_filter:
            conditions.append("p.level = %s")
            params.append(level_filter)

        if salary_min:
            conditions.append("e.salary >= %s")
            params.append(int(salary_min))

        if salary_max:
            conditions.append("e.salary <= %s")
            params.append(int(salary_max))

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        # Добавляем сортировку
        valid_sort_fields = ['id', 'first_name', 'last_name', 'position', 'level', 'hire_date', 'salary']
        if sort_field not in valid_sort_fields:
            sort_field = 'id'

        if sort_order not in ['ASC', 'DESC']:
            sort_order = 'ASC'

        sql += f" ORDER BY {sort_field} {sort_order}"

        # Выполняем запрос
        cursor.execute(sql, params)
        employees = cursor.fetchall()

        # Ограничиваем вывод 50 записями для удобства просмотра
        if len(employees) > 50:
            print(f"\n⚠️ Найдено {len(employees)} записей. Показаны первые 50.")
            employees = employees[:50]

        # Выводим результаты
        if employees:
            headers = ["ID", "Имя", "Фамилия", "Отчество", "Должность", "Уровень", "Дата приема", "Зарплата",
                       "Менеджер"]
            print(tabulate(employees, headers=headers, tablefmt="grid"))

            # Статистика
            print(f"\nВсего найдено: {len(employees)} сотрудников")
            if employees:
                salaries = [emp[7] for emp in employees]
                print(f"Средняя зарплата: {sum(salaries) / len(salaries):.2f}")
                print(f"Минимальная зарплата: {min(salaries)}")
                print(f"Максимальная зарплата: {max(salaries)}")
        else:
            print("❌ Сотрудники не найдены по заданным критериям")

    except ValueError:
        print("❌ Ошибка: некорректный формат числа для зарплаты")
    except Exception as e:
        print(f"❌ Ошибка при получении данных: {e}")
    finally:
        conn.close()


def add_employee():
    conn = connect_to_db()
    if conn:
        try:
            print("\nДобавление нового сотрудника:")
            first_name = input("Имя: ")
            last_name = input("Фамилия: ")
            middle_name = input("Отчество (если есть, иначе Enter): ") or None
            position_id = input("ID должности: ")
            hire_date = input("Дата приема (ГГГГ-ММ-ДД): ")
            salary = input("Зарплата: ")
            manager_id = input("ID менеджера (если есть, иначе Enter): ") or None

            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO employees 
                (first_name, last_name, middle_name, position_id, hire_date, salary, manager_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, middle_name, position_id, hire_date, salary, manager_id))

            conn.commit()
            print("✅ Сотрудник успешно добавлен")

        except Exception as e:
            print(f"❌ Ошибка при добавлении сотрудника: {e}")
        finally:
            conn.close()


def show_positions():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, level FROM positions ORDER BY id")
            positions = cursor.fetchall()

            headers = ["ID", "Должность", "Уровень"]
            print(tabulate(positions, headers=headers, tablefmt="grid"))

        except Exception as e:
            print(f"❌ Ошибка при получении данных: {e}")
        finally:
            conn.close()


def generate_hierarchy_positions():
    """Создает 5 уровней иерархии должностей"""
    positions = [
        (1, 'CEO', 'Executive'),
        (2, 'Директор департамента', 'Executive'),
        (3, 'Менеджер проекта', 'Senior'),
        (4, 'Тимлид', 'Middle'),
        (5, 'Старший разработчик', 'Middle'),
        (6, 'Разработчик', 'Junior'),
        (7, 'Тестировщик', 'Junior'),
        (8, 'Аналитик', 'Junior'),
        (9, 'Дизайнер', 'Junior'),
        (10, 'DevOps', 'Middle')
    ]
    return positions


def create_positions_table(conn):
    """Создает таблицу positions и заполняет её"""
    try:
        cursor = conn.cursor()

        # Очищаем таблицы если они существуют
        cursor.execute("DROP TABLE IF EXISTS employees CASCADE")
        cursor.execute("DROP TABLE IF EXISTS positions CASCADE")

        # Создаем таблицу positions
        cursor.execute("""
            CREATE TABLE positions (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                level VARCHAR(50) NOT NULL
            )
        """)

        # Заполняем таблицу positions
        positions = generate_hierarchy_positions()
        cursor.executemany(
            "INSERT INTO positions (id, title, level) VALUES (%s, %s, %s)",
            positions
        )

        conn.commit()
        print("✅ Таблица positions создана и заполнена")
        return positions

    except Exception as e:
        print(f"❌ Ошибка при создании таблицы positions: {e}")
        conn.rollback()
        return None


def create_employees_table(conn):
    """Создает таблицу employees"""
    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE employees (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                middle_name VARCHAR(100),
                position_id INTEGER REFERENCES positions(id),
                hire_date DATE NOT NULL,
                salary INTEGER NOT NULL,
                manager_id INTEGER REFERENCES employees(id)
            )
        """)

        conn.commit()
        print("✅ Таблица employees создана")
        return True

    except Exception as e:
        print(f"❌ Ошибка при создании таблицы employees: {e}")
        conn.rollback()
        return False


def generate_employees_data(num_employees=50000):
    """Генерирует тестовые данные для 50,000 сотрудников"""
    conn = connect_to_db()
    if not conn:
        return

    try:
        # Создаем таблицы
        positions = create_positions_table(conn)
        if not positions:
            return

        if not create_employees_table(conn):
            return

        cursor = conn.cursor()

        print("\n🔄 Создание иерархии сотрудников...")

        # 1. Создаем CEO (верхний уровень)
        print("👉 Создаем CEO...")
        cursor.execute("""
            INSERT INTO employees 
            (first_name, last_name, position_id, hire_date, salary)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (
            person.first_name(gender=Gender.MALE),
            person.last_name(gender=Gender.MALE),
            1,  # ID CEO
            dt.date(start=2010, end=2012),
            500000
        ))
        ceo_id = cursor.fetchone()[0]

        # 2. Создаем директоров департаментов (подчиняются CEO)
        print("👉 Создаем директоров департаментов...")
        directors = []
        for _ in range(5):
            cursor.execute("""
                INSERT INTO employees 
                (first_name, last_name, position_id, hire_date, salary, manager_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                person.first_name(),
                person.last_name(),
                2,  # ID директора
                dt.date(start=2012, end=2014),
                random.randint(200000, 300000),
                ceo_id
            ))
            directors.append(cursor.fetchone()[0])

        # 3. Создаем менеджеров проектов (подчиняются директорам)
        print("👉 Создаем менеджеров проектов...")
        managers = []
        for director_id in directors:
            for _ in range(random.randint(2, 4)):
                cursor.execute("""
                    INSERT INTO employees 
                    (first_name, last_name, position_id, hire_date, salary, manager_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    person.first_name(),
                    person.last_name(),
                    3,  # ID менеджера проекта
                    dt.date(start=2014, end=2016),
                    random.randint(150000, 200000),
                    director_id
                ))
                managers.append(cursor.fetchone()[0])

        # 4. Создаем тимлидов (подчиняются менеджерам проектов)
        print("👉 Создаем тимлидов...")
        team_leads = []
        for manager_id in managers:
            for _ in range(random.randint(2, 3)):
                cursor.execute("""
                    INSERT INTO employees 
                    (first_name, last_name, position_id, hire_date, salary, manager_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    person.first_name(),
                    person.last_name(),
                    4,  # ID тимлида
                    dt.date(start=2016, end=2018),
                    random.randint(100000, 150000),
                    manager_id
                ))
                team_leads.append(cursor.fetchone()[0])

        # 5. Создаем рядовых сотрудников (50,000)
        print(f"👉 Создаем {num_employees} рядовых сотрудников...")
        batch_size = 1000
        num_batches = num_employees // batch_size

        junior_positions = [6, 7, 8, 9]  # ID младших позиций
        middle_positions = [5, 10]  # ID средних позиций

        for batch in range(num_batches):
            employees_batch = []
            for _ in range(batch_size):
                # 80% - junior, 20% - middle
                if random.random() < 0.8:
                    position_id = random.choice(junior_positions)
                    salary = random.randint(40000, 80000)
                else:
                    position_id = random.choice(middle_positions)
                    salary = random.randint(80000, 120000)

                # Выбираем случайного менеджера (тимлида или менеджера)
                manager_pool = team_leads + managers
                manager_id = random.choice(manager_pool)

                employees_batch.append((
                    person.first_name(),
                    person.last_name(),
                    person.last_name() if random.random() > 0.3 else None,  # Отчество
                    position_id,
                    dt.date(start=2018, end=2023),
                    salary,
                    manager_id
                ))

            cursor.executemany("""
                INSERT INTO employees 
                (first_name, last_name, middle_name, position_id, hire_date, salary, manager_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, employees_batch)

            conn.commit()
            print(f"✅ Пакет {batch + 1}/{num_batches} ({len(employees_batch)} сотрудников) добавлен")

        print(f"\n🎉 Успешно сгенерировано {num_employees} сотрудников с 5 уровнями иерархии!")

    except Exception as e:
        print(f"❌ Ошибка при генерации данных: {e}")
        conn.rollback()
    finally:
        conn.close()


def main_menu():
    while True:
        print("\nГлавное меню:")
        print("1. Показать список сотрудников")
        print("2. Добавить сотрудника")
        print("3. Показать список должностей")
        print("4. Сгенерировать тестовые данные (50,000 сотрудников)")
        print("5. Выход")

        choice = input("Выберите действие (1-5): ")

        if choice == "1":
            show_employees()
        elif choice == "2":
            add_employee()
        elif choice == "3":
            show_positions()
        elif choice == "4":
            confirm = input("Вы уверены? Это перезапишет все существующие данные. (y/n): ")
            if confirm.lower() == 'y':
                generate_employees_data()
        elif choice == "5":
            print("Выход из программы")
            break
        else:
            print("❌ Неверный ввод, попробуйте снова")


if __name__ == "__main__":
    main_menu()