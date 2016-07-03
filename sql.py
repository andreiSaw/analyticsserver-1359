import sqlite3

with sqlite3.connect("sample.db") as connection:
    c=connection.cursor()
    c.execute("""DROP TABLE posts""")
    c.execute("""CREATE TABLE posts(title TEXT,description TEXT)""")
    c.execute('INSERT INTO posts VALUES ("admin","admin")')
    c.execute('INSERT INTO posts VALUES ("student","307307")')
    c.execute('INSERT INTO posts VALUES ("hseguest","hsepassword")')