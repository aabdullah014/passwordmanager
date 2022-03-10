import sqlite3

connection = sqlite3.connect('passwordlist.db')
cursor = connection.cursor()

def create_user(username, password):
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    cursor.execute(query, (username, password))
    connection.commit()
    connection.close()

def get_passwords(user_id):
    query = "SELECT website, username, password FROM passwords WHERE pass_id = ?"
    result = cursor.execute(query, (user_id,))
    row = result.fetchall()
    

    return row