#Name: Brendan Gee
#Date: 9/18/21
#Class: DSC450
#Assignment 1

# Part 1

# a.)
def avgNum(file):
    '''reads in a file with comma separated
    numbers and averages all the numbers in the file'''

    infile = open(file, 'r').read()
    infile = infile.split(', ')

    res = 0
    counter = 0
    for num in infile:
        res += int(num)
        counter += 1

    res /= counter

    return res

# b.)
def generateInsert(table, values):
    '''Given a table, insert record into as the values'''
    
    res = ', '.join(values)
            
    
    return 'INSERT INTO ' + table + ' VALUES (' + res + ');'
    
        
    
