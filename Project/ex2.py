import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        con = sqlite3.Connection('mydatabase.db')
        return con
    except Error:
        print(Error)

    return None


def sql_table(con):
    cursor_obj = con.cursor()
    cursor_obj.execute(
        """
    CREATE TABLE employees (
        id integer PRIMARY KEY,
        name text,
        salary real,
        department text,
        position text,
        hireDate text)
        """
    )

    con.commit()


if __name__ == "__main__":
    con = sql_connection()
    sql_table(con)
