import sqlite3


con = sqlite3.connect('mydatabase.db')


def sql_insert(con, entities):
    cursor_obj = con.cursor()
    cursor_obj.execute(
        """
    INSERT INTO employees(id, name, salary, department, position, hireDate)
    VALUES(?, ?, ?, ?, ?, ?)
    """,
        entities
    )
    con.commit()


entities = (2, 'Andrew', 800, 'IT', 'Tech', '2018-02-06')
sql_insert(con, entities)
