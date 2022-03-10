from random import seed
import sqlite3

connection = sqlite3.connect('users.db')
cur = connection.cursor()

create_user_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
cur.execute(create_user_table)

seed_users =[
    ['aabdullah014', 'King'],
    ['asahmad8','dad']
    ]

for users in seed_users:
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (users[0], users[1]))

connection.commit()
connection.close()

def post(username, password):
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()

    query = "INSERT INTO users VALUES (null, ?, ?)"

    cur.execute(query, (username, password))