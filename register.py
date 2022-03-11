import sqlite3


def create_user(username, password):
    connection = sqlite3.connect('passwordlist.db')
    cursor = connection.cursor()
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    cursor.execute(query, (str(username), str(password)))
    connection.commit()
    connection.close()

def get_passwords(user_id):
    connection = sqlite3.connect('passwordlist.db')
    cursor = connection.cursor()
    query = "SELECT website, username, password FROM passwords WHERE pass_id = ?"
    result = cursor.execute(query, (user_id,))
    row = result.fetchall()
    

    return row