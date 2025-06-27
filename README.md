## 📌 Возможности
- Генерация 50,000 тестовых записей сотрудников
- 5-уровневая иерархия должностей (CEO → Директор → Менеджер → Тимлид → Сотрудник)
- Фильтрация по:
  - Должности
  - Уровню
  - Диапазону зарплат
- Сортировка по любому полю

## 🛠 Технологии
- Python 3.8+
- PostgreSQL 13+
- Библиотеки:
  - `psycopg2` - работа с PostgreSQL
  - `tabulate` - красивые таблицы в консоли
  - `mimesis` - генерация тестовых данных

### 1. Клонирование репозитория
```bash
git clone https://github.com/larasedova/managment_system.git
cd management_system
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка БД
1. Установите PostgreSQL
2. Создайте базу данных:
```sql
CREATE DATABASE test;
CREATE USER postgres WITH PASSWORD '12345678';
GRANT ALL PRIVILEGES ON DATABASE hr_system TO hr_user;
```

### 4. Настройка окружения
Создайте файл `.env`:
```ini
DB_HOST=localhost
DB_PORT=5432
DB_NAME=test
DB_USER=postgres
DB_PASSWORD=12345678
```

## 🏃 Запуск
```bash
python main.py
```

## 📊 Примеры использования
1. Генерация тестовых данных:
   ```
   Выберите действие (1-5): 4
   ```

2. Фильтрация сотрудников:
   ```
   Должность: Разработчик
   Уровень: Junior
   Зарплата от: 50000
   ```


