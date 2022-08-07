#Name: Brendan Gee
#Date: 10/24/21
#Course: DSC450

import sqlite3

#create and insert into tables from part 2c

def createTables():
    '''creates a table view of 3 prejoined tables'''

    #setup connection to sqlite
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()

    #create tables
    query1 = '''create table Student (
StudentID Number,
Name VarChar2(50),
Address VarChar2(100),
GradYear Number(4),

Constraint Student_PK
Primary Key (StudentID)
);'''

    query2 = '''create table Course (
CName VarChar2(25),
Department VarChar2(25),
Credits Number(2),

Constraint Course_PK
Primary Key (CName)
);'''

    query3 = '''create table Grade (
CName VarChar2(25),
StudentID Number,
CGrade Number(1),

Constraint Grade_PK
Primary Key (CName, StudentID),

Constraint Course_FK1
Foreign Key (CName)
References Course (CName),

Constraint Course_FK2
Foreign Key (StudentID)
References Student (StudentID)
);'''

    #if table exists, drop, otherwise create
    queries = [['student',query1],['course',query2],['grade',query3]]
    for query in queries:
        try:
            cursor.execute(f'drop table {query[0]}')
        except:
            pass
        cursor.execute(query[1])
        

    #insert rows into tables
    studentrows = [[1,'Ash Ketchum', 'Pallet Town',2024],[2, 'Gary Oak', 'Pallet Town', 2024],
                   [3, 'Brock Harrison', 'Pewter City', 2021],[4, 'Misty Williams', 'Cerulean City', 2022],
                   [5, 'Jessie Murrow', 'Viridian City', 2025],[6, 'James Morgan', 'Viridian City', 2025]]

    courserows = [['Catching Pokemon', 'Beginner', 2],['Battle Tactics', 'Intermediate', 4],
                  ['Exploring Caves', 'Intermediate', 4],['Healing and Potions', 'Beginner', 2],
                  ['Gym Battles', 'Expert',6]]

    graderows = [['Catching Pokemon',1,3],['Catching Pokemon',2,4],['Catching Pokemon',3,2],
                 ['Catching Pokemon',4,3],['Battle Tactics',1,2],['Battle Tactics',2,4],
                 ['Battle Tactics',4,3],['Healing and Potions',3,3],['Gym Battles',1,3],
                 ['Gym Battles',2,4]]

    for row in studentrows:
        cursor.execute('Insert into student values (?, ?, ?, ?);', row)

    for row in courserows:
        cursor.execute('Insert into course values (?, ?, ?);', row)

    for row in graderows:
        cursor.execute('Insert into grade values (?, ?, ?);', row)
    #close/commit db
    conn.commit()
    conn.close()

#create a view that prejoins 3 tables from part 2c
def createView():
    '''creates a view that prejoins 3 tables from part 2c'''

    #setup connection to sqlite
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()

    #setup view query
    query1 = '''create view summary as
select grade.cname,grade.studentid,cgrade,name,address,gradyear,department,credits from student
left outer join grade on (grade.studentid = student.studentid)
left outer join course on (grade.cname = course.cname);'''

    #drop view if already created, otherwise create view
    try:
        cursor.execute(f'Drop view summary')
    except:
        pass
    cursor.execute(query1)

    #close/commit db
    conn.commit()
    conn.close()

#create a .txt file that uses the above query
def txtfile():
    '''takes the view and writes it into a .txt file'''

    #setup connection to sqlite
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()

    #open write file
    of = open('summary.txt', 'w')

    #grab all view data
    query1 = 'select * from summary'
    content = cursor.execute(query1)

    #place data into txt file
    for row in content:
        for i in range(len(row)):
            if i == 7:
                of.write(str(row[i]))
            else:
                of.write(str(row[i])+', ')
        of.write('\n')

    #close/commit db and txt file
    conn.commit()
    conn.close()
    of.close()

#find any violation of the functional dependency cname => credits
def catchFD():
    '''finds any FD violations of cname => credits and states them'''

    #open file, store content
    infile = open('summary.txt','r')
    content = infile.read().replace('\n',', ').split(', ')
    content = content[:-1]
    
    #put content into a list
    lst = []
    ans = []
    for i in range(len(content)):
        if i > 0 and (i+1) % 8 == 0:
            ans.append(content[i])
            lst.append(ans)
            ans = []
        else:
            ans.append(content[i])
            

    #go through each row and determine if the cname matches but credits don't
    res = []
    for i in range(len(lst)):
        for j in range(i,len(lst)):
            if lst[i][0] == lst[j][0] and lst[i][-1] != lst[j][-1]:
                res.append([i,j,lst[i][0]])

    #return result check
    for i in res:
        print(f'Lines {i[0]} and {i[1]} have a cname => credits FD error for course "{i[2]}"')

#run query for average grad year by department
def avgGradYear():
    '''finds the average grad year by department in summary table'''

    #open text file, store content
    infile = open('summary.txt','r')
    content = infile.read().replace('\n',', ').split(', ')
    content = content[:-1]

    #put content into a list
    lst = []
    ans = []
    for i in range(len(content)):
        if i > 0 and (i+1) % 8 == 0:
            ans.append(content[i])
            lst.append(ans)
            ans = []
        else:
            ans.append(content[i])

    #store averages by department in dictionary
    res = {}

    for row in lst:
        if row[-2] in res:
            res[row[-2]].append(int(row[-3]))
        else:
            res[row[-2]] = [int(row[-3])]

    #print statement with averages
    for key in res.keys():
        print(key, sum(res[key]) / len(res[key]))
    
        
        
        
    
    
        
