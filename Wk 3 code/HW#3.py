#Name: Brendan Gee
#Date: 10/3/21
#Assignment: HW#3
import sqlite3
def convertToCSV(db):
    '''converts a dbs rows into a comma separated value text file'''

    #connect to db
    conn = sqlite3.connect(db)
    c = conn.cursor()

    #write to file
    of = open('animal.txt', 'w')

    #select all contents of db
    content = c.execute('Select * from Animal;')

    #for loop writing to comma separated text file
    for row in content:
        for j in range(len(row)):
            if j == 3:
                of.write(str(row[j]))
            else:
                of.write(str(row[j]) + ', ')
        of.write('\n')

    #close/commit connection/file
    conn.commit()
    conn.close()
    of.close()

def convertToDB(infile):
    '''loads a CSV file into a sqlite database'''

    #get text file contents
    inf = open(infile, 'r')
    content = inf.read().replace('\n',', ').split(', ')

    #append content to a list of lists
    res = []
    temp = []
    for i in range(len(content)):
        if i != 0 and (i+1) % 4 == 0:
            temp.append(content[i])
            res.append(temp)
            temp = []
        else:
            temp.append(content[i])
            
    #connect to db
    conn = sqlite3.connect('dsc450.db')
    c = conn.cursor()

    #delete contents from db (in order to readd)
    c.execute('delete from animal;')

    #execute many dynamic statement
    c.executemany("INSERT INTO Animal VALUES (?, ?, ?, ?);", res)

    #select total rows
    ans = c.execute("Select count(*) from animal")
    return ans.fetchall()

    #close file & db
    conn.commit()
    conn.close()
    inf.close()

    

    


            
