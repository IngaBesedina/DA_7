#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import sqlite3
import typing as t
from pathlib import Path


"""
Вариант 2
Использовать словарь, содержащий следующие ключи: фамилия и инициалы;
номер группы; успеваемость(список из пяти элементов).Написать программу,
выполняющую следующие действия: ввод с клавиатуры данных в список, состоящий
из словарей заданной структуры; записи должны быть упорядочены по возрастанию
среднего балла; вывод на дисплей фамилий и номеров групп для всех студентов,
имеющих оценки 4 и 5; если таких студентов нет, вывести соответствующее
сообщение.Реализовать хранение данных в базе данных SQLite3.
Информация в базе данных должна храниться не менее чем в двух таблицах.
"""


def display_students(staff: t.List[t.Dict[str, t.Any]]) -> None:
    """
    Отобразить список студентов.
    """
    # Проверить, что список студентов не пуст.
    if staff:
        # Заголовок таблицы.
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 20, "-" * 14
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^14} |".format(
                "№", "Ф.И.О.", "Группа", "Оценки"
            )
        )
        print(line)

        # Вывести данные о всех студентах.
        for idx, student in enumerate(staff, 1):
            print(
                "| {:>4} | {:<30} | {:<20} | {:>14} |".format(
                    idx,
                    student.get("name", ""),
                    student.get("group", ""),
                    student.get("grades", ""),
                )
            )
        print(line)

    else:
        print("Список студентов пуст.")


def create_db(database_path: Path) -> None:
    """
    Создать базу данных.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Создать таблицу с информацией о группах.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_title TEXT NOT NULL
        )
        """
    )
    # Создать таблицу с информацией о студентах.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            group_id INTEGER NOT NULL,
            student_grades TEXT NOT NULL,
            FOREIGN KEY(group_id) REFERENCES groups(group_id)
        )
        """
    )
    conn.close()


def add_student(
    database_path: Path, name: str, group: str, grades: str
) -> None:
    """
    Добавить студента в базу данных.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Получить идентификатор имени в базе данных.
    # Если такой записи нет, то добавить информацию о новом имени.
    cursor.execute(
        """
        SELECT group_id FROM groups WHERE group_title = ?
        """,
        (group,),
    )
    row = cursor.fetchone()
    if row is None:
        4
        cursor.execute(
            """
            INSERT INTO groups (group_title) VALUES (?)
            """,
            (group,),
        )
        group_id = cursor.lastrowid
    else:
        group_id = row[0]

    # Добавить информацию о новом студенте.
    cursor.execute(
        """
        INSERT INTO students (student_name, group_id, student_grades)
        VALUES (?, ?, ?)
        """,
        (name, group_id, grades),
    )

    conn.commit()
    conn.close()


def select_all(database_path: Path) -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать всех студентов.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT students.student_name, groups.group_title,
        students.student_grades FROM students
        INNER JOIN groups ON groups.group_id = students.group_id
        """
    )
    rows = cursor.fetchall()

    data_with_avg = []
    for row in rows:
        grades = list(map(int, row[2].split(",")))
        average = sum(grades) / len(grades)
        data_with_avg.append((row[0], row[1], row[2], average))

    # Сортировка данных по среднему баллу
    sorted_data = sorted(data_with_avg, key=lambda x: x[3])

    conn.close()
    return [
        {
            "name": row[0],
            "group": row[1],
            "grades": row[2],
        }
        for row in sorted_data
    ]


def select_students(database_path: Path) -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать всех студентов, имеющих оценки 4 и 5.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # вывод на дисплей фамилий и групп для всех студентов, имеющих оценки 4 и 5
    # Извлечение данных из столбца базы данных
    cursor.execute(
        """
        SELECT students.student_name, groups.group_title,
        students.student_grades FROM students
        INNER JOIN groups ON groups.group_id = students.group_id
        """
    )
    rows = cursor.fetchall()

    selected_data = []
    for row in rows:
        grades = list(map(int, row[2].split(",")))
        if 2 not in grades and 3 not in grades:
            average = sum(grades) / len(grades)
            selected_data.append((row[0], row[1], row[2], average))

    selected_data = sorted(selected_data, key=lambda x: x[3])

    conn.close()

    return [
        {
            "name": row[0],
            "group": row[1],
            "grades": row[2],
        }
        for row in selected_data
    ]


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "--db",
        action="store",
        required=False,
        default=str(Path.home() / "students.db"),
        help="The database file name",
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("students")
    parser.add_argument(
        "--version", action="version", version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления студента.
    add = subparsers.add_parser(
        "add", parents=[file_parser], help="Add a new student"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The student's name",
    )
    add.add_argument(
        "-g", "--group", action="store", help="The student's group"
    )
    add.add_argument(
        "--grades", action="store", required=True, help="Grades received"
    )

    # Создать субпарсер для отображения всех студентов.
    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Display all students"
    )

    # Создать субпарсер для выбора студентов.
    _ = subparsers.add_parser(
        "select", parents=[file_parser], help="Select the students"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Получить путь к файлу базы данных.
    db_path = Path(args.db)
    create_db(db_path)

    # Добавить студента.
    if args.command == "add":
        add_student(db_path, args.name, args.group, args.grades)

    # Отобразить всех студентов.
    elif args.command == "display":
        display_students(select_all(db_path))

    # Выбрать требуемых студентов.
    elif args.command == "select":
        display_students(select_students(db_path))
        pass


if __name__ == "__main__":
    main()
