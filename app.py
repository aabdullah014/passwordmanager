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

    query = "SELECT username, password FROM users"
    username = user_txt.get()
    password = pass_txt.get()
    result = cursor.execute(query)
    row = result.fetchall()
    if username and password and (username, password) in row:
        query = "SELECT user_id FROM users WHERE username = ? AND password = ?"
        result = cursor.execute(query,(username, password))
        row = result.fetchone()
        validateUser(row[0], username, password)
    else:
        label.configure(text = "Please try again", fg = "red")

def refresh(username):
    connection = sqlite3.connect('passwordlist.db')
    cursor = connection.cursor()

    query = "SELECT user_id FROM users WHERE username = ? AND password = ?"
    username = user_txt.get()
    password = pass_txt.get()
    if username and password:
        result = cursor.execute(query,(str(username), str(password)))
        row = result.fetchone()
        loginSuccess(row, username)
    else:
        label.configure(text = "Please try again", fg = "red")

def create_credentials(website, username, password, user_id):
    root.withdraw()
    connection = sqlite3.connect('passwordlist.db')
    cursor = connection.cursor()
    query = "INSERT INTO passwords (website, username, password, pass_id) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (str(website), str(username), str(password), user_id))
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
    user_id = result.fetchone()
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
    btn_create = Button(root, text = "Create", fg = "blue", command = lambda: create_screen(user_id))

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

    login = (username, password)
    if login in row:
        root.withdraw()
        loginSuccess(user_id, username)
    else:
        label.configure(text = "Please try again", fg = "red")

def add_entry(website, username, password, user_id):
    connection = sqlite3.connect('passwordlist.db')
    cursor = connection.cursor()

    if username and password and website:
        root.quit()

        create_credentials(website, username, password, user_id)

        loginSuccess(user_id, username)    
        root.quit()

    else:
        label.configure(text = "Please try again", fg = "red")

    query = "SELECT * FROM passwords"
    result = cursor.execute(query)
    print(result.fetchall())

def create_screen(user_id):
    root1 = Tk()
    root1.title("Password Manager")
    root1.geometry('640x360')

    # label to root window e.g. text displayed
    label = Label(root1, text = "What would you like to add?")
    label.grid()

    # addition of entry field
    web_txt = Entry(root1, width = 20)
    user_txt = Entry(root1, width =20)
    pass_txt = Entry(root1, width = 20)
    web_txt.grid(column = 1, row = 2)
    user_txt.grid(column = 1, row = 3)
    pass_txt.grid(column = 1, row = 4)


    btn = Button(root1, text = "Add", fg = "black", command = lambda: add_entry(web_txt.get(), user_txt.get(), pass_txt.get(), user_id))
    btn.grid(column = 1, row = 5)



root.mainloop()