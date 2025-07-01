# 🏢 Employee Hierarchy Management System

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)
![Python](https://img.shields.io/badge/Python-3.7+-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

## 📝 Описание
Система для управления иерархией сотрудников компании с возможностью генерации тестовых данных. Проект реализует:

- Полноценную организационную структуру с 5 уровнями подчинения
- Генерацию 50,000+ реалистичных записей сотрудников
- Гибкие возможности фильтрации и сортировки данных
- Визуализацию данных в удобном табличном формате

## 🚀 Быстрый старт

### Предварительные требования
- Установленный PostgreSQL (версия 13+)
- Python 3.7+
- Пакеты из `requirements.txt`
- Библиотеки:
  - `psycopg2` - работа с PostgreSQL
  - `tabulate` - красивые таблицы в консоли
  - `mimesis` - генерация тестовых данных

### Установка
1. Создайте и активируйте виртуальное окружение:
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate    # Windows

2. Установка зависимостей
pip install -r requirements.txt

3. Настройка БД
- Установите PostgreSQL
- Создайте базу данных:
CREATE DATABASE test;
CREATE USER postgres WITH PASSWORD '12345678';
GRANT ALL PRIVILEGES ON DATABASE hr_system TO hr_user;

4. Настройка окружения
Создайте файл `.env`:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=test
DB_USER=postgres
DB_PASSWORD=12345678

5. Запуск
python main.py

## Функциональность
Основные команды
Команда						   Описание							      Пример
show_employees()			   Показать сотрудников с фильтрами	show_employees(limit=10)
add_employee()				   Добавить нового сотрудника			add_employee()
show_positions()			   Показать список должностей			show_positions()
generate_employees_data()	Генерация тестовых данных			generate_employees_data(50000)

## Примеры использования
- Показать топ-10 самых высокооплачиваемых сотрудников
show_employees(sort_field="salary", sort_order="DESC", limit=10)

- Найти всех разработчиков уровня Junior
show_employees(position_filter="Разработчик", level_filter="Junior")

- Добавить нового сотрудника
add_employee(
    first_name="Иван",
    last_name="Петров",
    position_id=6,
    hire_date="2023-01-15",
    salary=75000,
    manager_id=42
)

## Структура базы данных

- Таблица positions
Поле			     Тип					  Описание
id				     SERIAL				  Уникальный идентификатор
title			     VARCHAR(100)		Название должности
level			     VARCHAR(50)		Уровень (Junior/Middle/Senior/Executive)

- Таблица employees
Поле			     Тип					  Описание
id				     SERIAL				  Уникальный идентификатор
first_name		VARCHAR(100)		Имя
last_name		  VARCHAR(100)		Фамилия
middle_name		VARCHAR(100)		Отчество
position_id		INTEGER				  Ссылка на должность
hire_date		  DATE				    Дата приема
salary			  INTEGER				  Зарплата
manager_id		INTEGER				  Ссылка на руководителя

## Тестирование

- генерация тестовых данных
python -c "from main import generate_employees_data; generate_employees_data(1000)"

- проверка целостности данных
psql -d employee_db -c "SELECT COUNT(*) FROM employees;"
psql -d employee_db -c "SELECT level, COUNT(*) FROM positions JOIN employees ON positions.id = employees.position_id GROUP BY level;"

## Производительность

Генерация 50,000 записей: ~3 минуты
Среднее время запроса: < 1 секунды
Поддерживает организации до 100,000 сотрудников
