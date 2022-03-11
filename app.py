from audioop import add
from tkinter import *
import sqlite3
from venv import create
from password import updateLogin, deleteLogin
import user
from register import create_user, get_passwords

# create root window
root = Tk()

# root window title and dimension
root.title("Password Manager")
root.geometry('640x360')

# label to root window e.g. text displayed
label = Label(root, text = "Welcome to the Password Manager. Please Login below.")
label.grid()

# addition of entry field
user_txt = Entry(root, width = 20)
pass_txt = Entry(root, width = 20)
user_txt.grid(column = 1, row = 3)
pass_txt.grid(column = 1, row = 4)

# function to display text when button clicked
def clicked():
    connection = sqlite3.connect('passwordlist.db')
    cursor = connection.cursor()

    query = "SELECT user_id FROM users WHERE username = ? AND password = ?"
    username = user_txt.get()
    password = user_txt.get()
    result = cursor.execute(query,(username, password))
    row = result.fetchone()[0]
    validateUser(row, username, password)

def refresh(username):
    connection = sqlite3.connect('passwordlist.db')
    cursor = connection.cursor()

    query = "SELECT user_id FROM users WHERE username = ? AND password = ?"
    username = user_txt.get()
    password = user_txt.get()
    result = cursor.execute(query,(str(username), str(password)))
    user_id = result.fetchone()[0]
    loginSuccess(user_id, username)

def create_credentials(website, username, password):
    root.withdraw()
    connection = sqlite3.connect('passwordlist.db')
    cursor = connection.cursor()
    query = "INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)"
    cursor.execute(query, (str(website), str(username), str(password)))
    connection.commit()
    connection.close()

def register(username, password):
    create_user(username, password)
    connection = sqlite3.connect('passwordlist.db')
    cursor = connection.cursor()

    query = "SELECT user_id FROM users WHERE username = ? AND password = ?"
    username = user_txt.get()
    password = user_txt.get()
    result = cursor.execute(query,(username, password))
    user_id = result.fetchone()[0]

    query = "SELECT * FROM users"
    result = cursor.execute(query)

    loginSuccess(user_id, username)

# create button
btn = Button(root, text = "Login", fg = "black", command= clicked)
btn.grid(column = 1, row = 5)

# create button
btn = Button(root, text = "Register", fg = "black", command= lambda: register(user_txt.get(), pass_txt.get()))
btn.grid(column = 1, row = 6)

# if login successful, list the website
def loginSuccess(user_id, username):
    con = sqlite3.connect('passwordlist.db')
    cursorObj = con.cursor()

    root = Tk()

    root.title("Password Manager")
    root.geometry('1280x720')

    label = Label()
    label.configure(text = "Please click on a Website/Service to obtain login information.")
    label.grid()

    # btn_update = Button(root, text = "Update", fg = "blue", command = clicked)
    # btn_delete = Button(root, text = "Delete", fg = "blue", command = clicked)
    btn_refresh = Button(root, text = "Refresh", fg = "blue", command = lambda: refresh(username))
    btn_create = Button(root, text = "Create", fg = "blue", command = lambda: create_screen(username))

    # btn_update.grid(column = 0, row = 1)
    # btn_delete.grid(column = 1, row = 1)
    btn_refresh.grid(column = 1, row = 1)
    btn_create.grid(column = 2, row = 1)

    
    query = "SELECT * FROM passwords WHERE pass_id = ?"
    result = cursorObj.execute(query, (user_id,))
    row = result.fetchall()
    for i in range(len(row)):
        web = Label(root, text = "Website: "+str(row[i][0]))
        web.grid(row = i+5, column = 5)
        user = Label(root, text = "Username: "+str(row[i][1]))
        user.grid(row = i+5, column = 10)
        passw = Label(root, text = "Password: "+str(row[i][2]))
        passw.grid(row = i+5, column = 15)
    
def validateUser(user_id, username, password):
    con = sqlite3.connect('passwordlist.db')
    cursor = con.cursor()

    query = "SELECT username, password FROM users"
    result = cursor.execute(query)
    row = result.fetchall()
    print(row)

    login = (username, password)
    if login in row:
        root.withdraw()
        loginSuccess(user_id, username)
    else:
        label.configure(text = "Please try again", fg = "red")

def add_entry(website, username, password):
    connection = sqlite3.connect('passwordlist.db')
    cursor = connection.cursor()

    query = "SELECT user_id FROM users WHERE username = ? AND password = ?"
    username = user_txt.get()
    password = user_txt.get()
    result = cursor.execute(query,(username, password))
    user_id = result.fetchone()[0]
    create_credentials(website, username, password)

    loginSuccess(user_id, username)

def create_screen(username):
    root = Tk()
    root.title("Password Manager")
    root.geometry('640x360')

    # label to root window e.g. text displayed
    label = Label(root, text = "What would you like to add?")
    label.grid()

    # addition of entry field
    web_txt = Entry(root, width = 20)
    user_txt = Entry(root, width =20)
    pass_txt = Entry(root, width = 20)
    web_txt.grid(column = 1, row = 3)
    user_txt.grid(column = 1, row = 2)
    pass_txt.grid(column = 1, row = 4)


    btn = Button(root, text = "Add", fg = "black", command = lambda: add_entry(web_txt.get(), user_txt.get(), pass_txt.get()))
    btn.grid(column = 1, row = 5)



root.mainloop()