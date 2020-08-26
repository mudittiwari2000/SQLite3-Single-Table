import sqlite3


def dbConnect():
    conn = sqlite3.connect('orgCountDB.sqlite')
    cur = conn.cursor()  # Creating a cursor to execute SQL

    # Dropping/Deleting the Table if it already exists
    cur.execute('''
        DROP TABLE IF EXISTS Counts
    ''')

    # Creating a Table named Counts with 2 attributes
    cur.execute('''
        CREATE TABLE Counts (
            org TEXT,
            count INTEGER
        )
    ''')
    return cur, conn


def readingFile(cur, conn):
    filename = input('Enter the File Name: ')
    if len(filename) < 1:
        filename = 'mbox1.txt'
    fHandle = open(filename)
    for line in fHandle:
        if not line.startswith('From') or line.startswith('From:'):
            continue
        line = line.strip()
        org = line.split()[1].split('@')[1]
        # print (org, end=', ')
        cur.execute('SELECT * FROM Counts WHERE org = ?', (org,))
        row = cur.fetchone()
        if row is None:
            cur.execute('''
                INSERT INTO Counts (org, count) VALUES (?, 1)
            ''', (org,))
        else:
            cur.execute('''
                UPDATE Counts SET count = count + 1 WHERE org = ?
            ''', (org,))

    conn.commit()

    sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC'

    for row in cur.execute(sqlstr):
        print(str(row[0]), row[1])

    cur.close()

def main ():
    cursor, connection = dbConnect()
    readingFile(cursor, connection)

if __name__ == '__main__':
    main()
