import sqlite3


con = sqlite3.connect('mydatabase.db')


def sql_fetch(con):
    cursor_obj = con.cursor()
    cursor_obj.execute("SELECT * FROM employees")
    [print(row) for row in cursor_obj.fetchall()]


sql_fetch(con)
