import sqlite3

def main():
    getTable()

def connect():
    conn = None
    try:
        conn = sqlite3.connect('MLBData.db')
        return conn
    except sqlite3.Error as e:
            print(e)
    return conn


def createTable():
    conn = sqlite3.connect(r"C:\Users\samue\Downloads\sqlitestudio-3.3.3\SQLiteStudio\FILES\MLBData.db")
    sql_statement = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """
    if conn is not None:
        conn.cursor().execute(sql_statement)
    else:
        print("Error! cannot create the database connection.")

def getTable():
    conn = sqlite3.connect(r"C:\Users\samue\Downloads\sqlitestudio-3.3.3\SQLiteStudio\FILES\MLBData.db")

    sql_statement = "SELECT ID FROM DataTest"

    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(sql_statement)
        response = cursor.fetchall()
        print(response)
    else:
        print("Error! cannot create the database connection.")


main()