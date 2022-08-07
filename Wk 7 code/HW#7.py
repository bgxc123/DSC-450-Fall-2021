#Name: Brendan Gee
#Date: 10/31/21
#Assignment: HW#7

import pandas
import numpy
import random
import sqlite3
import urllib.request
import json
#Part1
#a.)
def randNumbers(x):
    '''generates x random numbers between 33 and 100'''

    res = []
    randNums = numpy.arange(33,101)
    for i in range(x):
        
        num = random.choice(randNums)
        res.append(num)

    return res

#b.)
##nums = randNumbers(60)
##>>> res = pandas.Series(nums)
##>>> res[res < 37]
##5     36
##14    33
##19    33
##dtype: int64

#c.)
##>>> res2 = numpy.array(nums)
##>>> res2 = np.reshape(res2,(6,10))
##>>> res2
##array([[ 93,  87,  89,  55,  61,  36,  66,  70,  96,  46],
##       [ 88,  44,  96,  93,  33,  91,  76,  72,  75,  33],
##       [ 95,  64,  51,  64,  83,  80,  46,  50,  90,  57],
##       [ 93,  65,  92,  48,  79,  76,  41,  85,  96,  98],
##       [ 52,  78,  92,  73, 100,  74,  81,  50,  37,  74],
##       [ 96,  71,  68,  63,  99,  58,  90,  54,  79,  69]])
##>>> np.where(res2>=50,50,res2)
##array([[50, 50, 50, 50, 50, 36, 50, 50, 50, 46],
##       [50, 44, 50, 50, 33, 50, 50, 50, 50, 33],
##       [50, 50, 50, 50, 50, 50, 46, 50, 50, 50],
##       [50, 50, 50, 48, 50, 50, 41, 50, 50, 50],
##       [50, 50, 50, 50, 50, 50, 50, 50, 37, 50],
##       [50, 50, 50, 50, 50, 50, 50, 50, 50, 50]])

#Part2
#a.) & b.)
def createTables():
    '''creates the mod 5 modified table and mod 7 table'''

    #set sqlite3 connection
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()

    #mod 7 table
    usersTable = '''create table users (
id number,
name VarChar2(50),
screen_name VarChar2(50),
description VarChar2(100),
friends_count number,
primary key (id)
);'''
    #mod 5 table
    tweetsTable = '''create table tweets (
created_at Date,
id_str Char(18),
text VarChar2(280),
source VarChar2(200),
in_reply_to_user_id VarChar2(20),
in_reply_to_screen_name VarChar2(50),
in_reply_to_status_id Char(18),
retweet_count Number,
contributors VarChar2(50),
user_id number,

primary key (id_str),
foreign key (user_id)
references users(id)
);'''
    tables = [[usersTable,'users'],[tweetsTable,'tweets']]

    #create / drop tables
    for table in tables:
        try:
            cursor.execute(f'drop table {table[1]}')
        except:
            pass
        cursor.execute(table[0])

    #connect to txt file hyperlink
    webFD = urllib.request.urlopen('https://dbgroup.cdm.depaul.edu/DSC450/Module7.txt')
    allTweets = webFD.readlines()
    #load table / write errored tweets to write file

    ##error file
    outfile = open('Module7_errors.txt','a')

    ##for loop to read tweets
    for tweet in allTweets:
        #check for error tweets and append to error file
        try:
            tdict = json.loads(tweet.decode('utf8'))
        except ValueError:
            outfile.write(tweet.decode('utf8'))
            continue
        #load user/tweet data into a list before inserting
        userData = [tdict['user']['id'], tdict['user']['name'], tdict['user']['screen_name'],
                    tdict['user']['description'], tdict['user']['friends_count']]

        tweetData = [tdict['created_at'], tdict['id_str'], tdict['text'],
                    tdict['source'], tdict['in_reply_to_user_id'],
                    tdict['in_reply_to_screen_name'], tdict['in_reply_to_status_id'],
                    tdict['retweet_count'], tdict['contributors'], tdict['user']['id']]

        #convert nulls or blanks to None type
        for i in range(len(userData)):
            if userData[i] == '' or userData[i] == 'NULL':
                userData[i] = None
        for j in range(len(tweetData)):
            if tweetData[j] == '' or tweetData[j] == 'NULL':
                tweetData[j] = None

        #insert into table
        cursor.execute('Insert or Ignore into users values (?, ?, ?, ?, ?);',userData)
        cursor.execute('Insert or Ignore into tweets values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', tweetData)

    #close files / connections
    conn.commit()
    conn.close()
    outfile.close()
        
            
