import sqlite3 as sql
import pandas as pd

conn = sql.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE employee (
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT
    );""")

conn.commit()

cursor.execute("INSERT INTO employee VALUES (1,'john');")
