import sqlite3


con = sqlite3.connect('mydatabase.db')


def sql_update(con):
    cursor_obj = con.cursor()
    cursor_obj.execute(
        "UPDATE employees SET name = 'Rogers' where id = 2"
    )
    con.commit()


sql_update(con)
