#Name: Brendan Gee
#Date: 11/14/21
#Assignment: Module 9

import urllib.request
import sqlite3
import json
import time
import matplotlib.pyplot as plt

#Tables from Module 7
def createTables():
    '''creates the mod 5 modified table and mod 7 table'''

    #set sqlite3 connection
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()

    #mod 7 table - users
    usersTable = '''create table users (
id number,
name VarChar2(50),
screen_name VarChar2(50),
description VarChar2(100),
friends_count number,
primary key (id)
);'''

    #mod 9 table - geo
    geoTable = '''create table geo (
id number,
type varchar2(20),
longitude number,
latitude number,

constraint geo_pk
primary key (id)
);'''
    #mod 5 table - tweets
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
geo_id number,

primary key (id_str),
foreign key (user_id)
references users(id),
foreign key (geo_id)
references geo(id)
);'''
    tables = [[usersTable,'users'],[geoTable, 'geo'],[tweetsTable,'tweets']]

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
    counter = 1
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
                    tdict['retweet_count'], tdict['contributors'], tdict['user']['id'],
                     counter]
        if tdict['geo'] != None:
            geoData = [counter, tdict['geo']['type'], tdict['geo']['coordinates'][0],
                       tdict['geo']['coordinates'][1]]
            cursor.execute('Insert or Ignore into geo values (?, ?, ?, ?);', geoData)
            

        #convert nulls or blanks to None type
        for i in range(len(userData)):
            if userData[i] == '' or userData[i] == 'NULL':
                userData[i] = None
        for j in range(len(tweetData)):
            if tweetData[j] == '' or tweetData[j] == 'NULL':
                tweetData[j] = None

        #insert into table
        cursor.execute('Insert or Ignore into users values (?, ?, ?, ?, ?);',userData)
        cursor.execute('Insert or Ignore into tweets values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', tweetData)
        counter += 1

    #close files / connections
    conn.commit()
    conn.close()
    outfile.close()

#a.) time how long it takes to select tweets with id_strs that have 88 or 777 in them

def timeIDs():
    '''calculates the amount of time it takes to retrieve certain ids'''

    #start time
    start = time.time()
    
    #connect to DB, start the time
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()
    query1 = '''select * from tweets where ((id_str like '%777%') or (id_str like '%88%'));'''

    
    print(cursor.execute(query1).fetchall())
    #end time, record time it took
    end = time.time()
    print("Elapsed Time: "+ str(end - start))


#b.) do the above calculation without using sqlite

def pyTimeIDs():
    '''calculates the amount of time it takes to receive data without using sqlite'''
    start = time.time()
    #open tweet file
    webFD = urllib.request.urlopen('https://dbgroup.cdm.depaul.edu/DSC450/Module7.txt')
    allTweets = webFD.readlines()

    res = []

    for tweet in allTweets:
        try:
            
            tdict = json.loads(tweet.decode('utf8'))

            if '88' in tdict['id_str'] or '777' in tdict['id_str']:
                res.append(tdict['id_str'])
        except:
            continue

    print(res)
    end = time.time()
    print("Elapsed Time: "+ str(end-start))

#c.) Find the number of unique values in "in_reply_to_user_id"

def uniqueSQL():
    '''finds the unique values in a given field'''

    start = time.time()

    #connect to db, query
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()
    

    query1 = '''select count(distinct in_reply_to_user_id) from tweets;'''

    print(cursor.execute(query1).fetchall())

    end = time.time()
    print("Elapsed Time: "+ str(end-start))

#d.)
def uniquePy():
    '''finds the unique value of a given field w/out SQLite'''

    start = time.time()
    #open tweet file
    webFD = urllib.request.urlopen('https://dbgroup.cdm.depaul.edu/DSC450/Module7.txt')
    allTweets = webFD.readlines()

    res = []

    for tweet in allTweets:
        try:
            tdict = json.loads(tweet.decode('utf8'))

            if tdict['in_reply_to_user_id'] not in res:
                res.append(tdict['in_reply_to_user_id'])
        except:
            continue

    print(len(res))
    end = time.time()
    print("Elapsed Time: "+ str(end-start))

#e.)

def plotTweetLengths():
    '''plot the length of tweets vs username lengths'''
    
    #open tweet file
    webFD = urllib.request.urlopen('https://dbgroup.cdm.depaul.edu/DSC450/Module7.txt')
    allTweets = webFD.readlines()

    tweetLen = []
    userLen = []
    counter = 0

    #compile lengths of first 40 tweets & usernames
    for tweet in allTweets:
        if counter == 40:
            break
        try:
            
            tdict = json.loads(tweet.decode('utf8'))

            tweetLen.append(len(tdict['text']))
            userLen.append(len(tdict['user']['name']))
            counter += 1

        except:
            continue

    #plot scatterplots
    fig = plt.figure()
    sp1 = fig.add_subplot(1,1,1)
    sp1.scatter(tweetLen, userLen)
    plt.title('Tweet Length vs Username Length')
    plt.xlabel('Tweet Length')
    plt.ylabel('Username Length')
    plt.show()
        

    

