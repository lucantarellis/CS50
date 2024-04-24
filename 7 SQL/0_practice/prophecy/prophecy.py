import csv
from cs50 import SQL

db = SQL("sqlite:///roster.db")
db.execute("DROP TABLE IF EXISTS students")
db.execute("CREATE TABLE IF NOT EXISTS re_students (id INTEGER, student_name TEXT, PRIMARY KEY(id))")
db.execute("CREATE TABLE IF NOT EXISTS houses (id INTEGER, house_name TEXT, head TEXT, PRIMARY KEY(id), UNIQUE(house_name, head))")
db.execute("CREATE TABLE IF NOT EXISTS relationships (id INTEGER, student_name TEXT, house_name TEXT, PRIMARY KEY(id))")


with open("./students.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
            db.execute("INSERT OR IGNORE INTO re_students (student_name) VALUES (?)", row["student_name"])
            db.execute("INSERT OR IGNORE INTO relationships (student_name, house_name) VALUES (?, ?)", row["student_name"], row["house"])
            db.execute("INSERT OR IGNORE INTO houses (house_name, head) VALUES (?, ?)", row["house"], row["head"])