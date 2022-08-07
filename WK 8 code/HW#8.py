#Name: Brendan Gee
#Date: 11/7/21
#Assignment: Module 8

import pandas

#a.) Find all female employees

def femaleEmployees():
    '''finds the female employees in a df and returns them'''

    #read in .txt file
    df = pandas.read_csv('Employee.txt',names=['fname','mname','lname'
                                              ,'id','dob','address','city',
                                              'state','sex','salary','sup_id',
                                              'dept'])

    #return female employees using the created df
    res = df[df['sex'] == 'F']

    return res

#b.) Find the lowest salary for male employees

def minSalaryMale():
    '''finds the male employee with the lowest salary'''

    #read in .txt file
    df = pandas.read_csv('Employee.txt',names=['fname','mname','lname'
                                              ,'id','dob','address','city',
                                              'state','sex','salary','sup_id',
                                              'dept'])
    #isolate male employees in df2
    df2 = df[df['sex']=='M']

    #find the min salary of df2
    res = min(df2['salary'])

    return res

#c.) For each middle initial, print all of the salaries in that group

def salaryByMidInit():
    '''prints out each salary by middle initial'''

    #read in .txt file
    df = pandas.read_csv('Employee.txt',names=['fname','mname','lname'
                                              ,'id','dob','address','city',
                                              'state','sex','salary','sup_id',
                                              'dept'])

    #for loop
    for name,value in df['salary'].groupby(df['mname']):
        print('Middle Initial: ', name)
        print('Salary: ', value)
        print('-'*30)
