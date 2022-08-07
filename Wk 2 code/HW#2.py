def validateInsert(statement):
    '''checks if user is inputting correct insert SQL statement'''
    res = statement.split()

    #finds the values in the user input
    values = findParentheses(statement)

    if statement[:11].lower() == 'insert into' and statement[-1] == ';':
        
        return f'Inserting {values} into {res[2]} table'

    else:
        return 'Invalid insert'
    

def findParentheses(string):
    '''finds the first pair of open/closed parathesis'''
    res = ''
    start = False
    counter = 0

    while len(string) > counter:
        if string[counter] == '(':
            start = True
        elif string[counter] == ')':
            start = False

        if start:
            res += string[counter]

        counter += 1

    res += ')'

    return res
                                            
            
