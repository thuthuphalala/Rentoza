import sqlite3
con = sqlite3.connect("MoonshinePatronsDb.db")

#con.execute("CREATE TABLE Patrons(ID, Name, Gender, Weight, Drinks, BAC, LastDrink, Threshold)")

def AddPatron(ID, Name, Gender, Weight):
    conn = sqlite3.connect('MoonshinePatronsDb.db')

    conn.execute("""INSERT INTO Patrons (ID, Name, Gender, Weight, Drinks, BAC, LastDrink, Threshold)
          VALUES ({}, {}, {}, {}, 0, 0, 0, 0)""".format(ID, Name, Gender, Weight))
    conn.commit()
    conn.close()

def GetPatronDetails(idNo):
    conn = sqlite3.connect('MoonshinePatronsDb.db')
    cursor = conn.execute("SELECT * from Patrons where ID = {}".format(idNo))
    return cursor

def GetTopBacPatronDetails():
    conn = sqlite3.connect('MoonshinePatronsDb.db')
    cursor = conn.execute("SELECT * From Patrons ORDER BY BAC DESC")
    return cursor

def DeletePatron(id):
    conn = sqlite3.connect('MoonshinePatronsDb.db')
    conn.execute("DELETE from Patrons where ID = {};".format(id))
    conn.commit()
    conn.close()

def UpdatePatron(idNo,drinks,bac,lastDrink,Threshold):
    conn = sqlite3.connect('MoonshinePatronsDb.db')
    conn.execute("UPDATE Patrons set Drinks = {}, BAC = {}, LastDrink = {}, Threshold = {} where ID = {}".format(drinks,bac,lastDrink,Threshold,idNo))
    conn.commit()
    conn.close()
