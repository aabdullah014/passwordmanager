import sqlite3

con = sqlite3.connect('passwordlist.db')
cursorObj = con.cursor()

cursorObj.execute("CREATE TABLE IF NOT EXISTS passwords (website text, username text, password text)")

def insertLogin (website, username, password):
    login = (website, username, password)
    cursorObj.execute("INSERT INTO passwords(website, username, password) VALUES (?, ?, ?)", login)
    con.commit()

def getLogin (website):
    cursorObj.execute("SELECT username, password FROM passwords WHERE website = ?", (website,))
    retreivedCred = cursorObj.fetchall()

    print(retreivedCred)

def updateLogin (website, username, password):
    with con:
        cursorObj.execute("UPDATE passwords SET username = :username, password = :password WHERE website = :website",
            {'website': website, 'username': username, 'password': password})

def deleteLogin (website):
    with con:
        cursorObj.execute("DELETE from passwords WHERE website = :website", {'website': website})
