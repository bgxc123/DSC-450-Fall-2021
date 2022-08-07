#Name: Brendan Gee
#Date: 10/11/21
#Assignment: #4

import sqlite3

def tigerNotCommon(infile):
    '''finding the names of the animals related to tiger and are not common'''
    inf = open('animal.txt','r')
    content = inf.readlines()

    for row in content:
        row = row.strip().split(', ')

        if 'tiger' in row[1] and 'common' not in row[2]:
            print(row[1])
    inf.close()

def notTiger(infile):
    '''find the names of the animals not related to tiger'''

    inf = open('animal.txt','r')
    content = inf.readlines()

    for row in content:
        row = row.strip().split(', ')

        if 'tiger' not in row[1]:
            print(row[1])

    inf.close()



def insertRows(infile):
    '''inserts the rows into the respective tables based on the txt file'''

    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()

    inf = open(infile, 'r')
    content = inf.readlines()
    tables = ['name','job','work']
    tableCreate = ['''create table Job
(
Job VarChar2(20), Salary Number, Assistant VarChar2(20),
Constraint Job_PK
Primary Key (Job)
);''', '''create table Name
( First VarChar2(25), Last VarChar2(25), Address VarChar2(50),
  Constraint Name_PK
  Primary Key (First, Last)
);''', '''create table Work
(
First VarChar2(25), Last VarChar2(25), Job VarChar2(20),
Constraint Work_PK
Primary Key (First, Last, Job),

Constraint First_FK
Foreign Key (First,Last)
References Name(First,Last),

Constraint Job_FK
Foreign Key (Job)
References Job(Job)

);''']

    #drop tables if they exist, then create table
    for table in tables:
        
        try:
        
            cursor.execute(f'Drop table {table};')
        except:
            pass

    for tableCode in tableCreate:
        cursor.execute(tableCode)
        

    #insert into job table
    for row in content:

        row = row.strip().split(', ')
        jobData = row[3:]
        for i in range(len(jobData)):
            if jobData[i] == 'NULL':
                jobData[i] = None
                
        cursor.execute("Insert or Ignore into Job values (?, ?, ?)",jobData)

    #insert into name table
    for row in content:

        row = row.strip().split(', ')
        nameData = row[:3]
        for i in range(len(nameData)):
            if nameData[i] == 'NULL':
                nameData[i] = None
        cursor.execute("Insert or Ignore into Name values (?, ?, ?)",nameData)

    #insert into work table
    for row in content:

        row = row.strip().replace('NULL','None').split(', ')
        workData = [row[0],row[1],row[3]]
        for i in range(len(workData)):
            if workData[i] == 'NULL':
                workData = None
        cursor.execute("Insert or Ignore into Work values (?, ?, ?)",workData)

    #close out files
    conn.commit()
    conn.close()
    inf.close()
    
    

    

    
