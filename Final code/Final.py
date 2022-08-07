#Name: Brendan Gee
#Date: 11/23/21
#Assignment: Final

import urllib.request
import sqlite3
import json
import time
import matplotlib.pyplot as plt
import re

#Part 1
##a.)
def downloadTweets(of,c):
    '''puts 60,000 and 600,000 tweets into two .txt files'''

    #connect to txt file hyperlink
    webFD = urllib.request.urlopen('http://dbgroup.cdm.depaul.edu/DSC450/OneDayOfTweets.txt')


    #write into file
    outfile1 = open(of,'w')
    counter = 0

    #capture tweets into each respective .txt file
    for tweet in webFD:
        
        if counter < c:
            outfile1.write(tweet.decode('utf8')+'\n')
            counter += 1
        else:
            break
            


    #close out text files
    outfile1.close()

##b.)
def maxString():
    '''Find max string length for specified fields'''

    #open file
    infile = open('600ktweets.txt','r')
    allTweets = infile.read().split('\n')
    infile.close()

    #store max lengths in list
    resLst = [0,0,0,0]

    #for each tweet, store string length if it's bigger than resLst current
    for tweet in allTweets:

        #json load
        try:
            tdict = json.loads(tweet)
        except:
            continue
        if tdict['text'] == None:
            tdict['text'] = ''
        if tdict['in_reply_to_user_id_str'] == None:
            tdict['in_reply_to_user_id_str'] = ''
        if tdict['in_reply_to_screen_name'] == None:
            tdict['in_reply_to_screen_name'] = ''
        if tdict['user']['screen_name'] == None:
            tdict['user']['screen_name'] = ''
        
        len0 = len(tdict['text'])
        len1 = len(tdict['in_reply_to_user_id_str'])
        len2 = len(tdict['in_reply_to_screen_name'])
        len3 = len(tdict['user']['screen_name'])
        #check string lengths
        if len0 > resLst[0]:
            resLst[0] = len0

        if len1 > resLst[1]:
            resLst[1] = len1

        if len2 > resLst[2]:
            resLst[2] = len2

        if len3 > resLst[3]:
            resLst[3] = len3
    print(f'Tweet table text max length is {resLst[0]}')
    print(f'Tweet table in_reply_to_user_id max length is {resLst[1]}')
    print(f'Tweet table in_reply_to_screen_name max length is {resLst[2]}')
    print(f'User table screen_name max length is {resLst[3]}')

##c.)
def webCreateTables(tweetCount):
    '''creates a table loaded from the day of tweets'''

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
text VarChar2(450),
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
    webFD = urllib.request.urlopen('http://dbgroup.cdm.depaul.edu/DSC450/OneDayOfTweets.txt')
    #load table / counter & tweet requirement
    geoID = 1
    counter = 0
    tweetRequirement = tweetCount
    #for loop to read tweets
    for tweet in webFD:
        if counter < tweetRequirement:
            #check for error tweets and append to error file
            try:
                tdict = json.loads(tweet.decode('utf8'))
            except ValueError:
                continue
            #load user/tweet data into a list before inserting
            if tdict['geo'] == None:
                
                userData = [tdict['user']['id'], tdict['user']['name'], tdict['user']['screen_name'],
                            tdict['user']['description'], tdict['user']['friends_count']]

                tweetData = [tdict['created_at'], tdict['id_str'], tdict['text'],
                            tdict['source'], tdict['in_reply_to_user_id'],
                            tdict['in_reply_to_screen_name'], tdict['in_reply_to_status_id'],
                            tdict['retweet_count'], tdict['contributors'], tdict['user']['id'],
                             None]
            else:
                userData = [tdict['user']['id'], tdict['user']['name'], tdict['user']['screen_name'],
                            tdict['user']['description'], tdict['user']['friends_count']]

                tweetData = [tdict['created_at'], tdict['id_str'], tdict['text'],
                            tdict['source'], tdict['in_reply_to_user_id'],
                            tdict['in_reply_to_screen_name'], tdict['in_reply_to_status_id'],
                            tdict['retweet_count'], tdict['contributors'], tdict['user']['id'],
                             geoID]
                geoData = [geoID, tdict['geo']['type'], tdict['geo']['coordinates'][0],
                           tdict['geo']['coordinates'][1]]
                cursor.execute('Insert or Ignore into geo values (?, ?, ?, ?);', geoData)
                geoID += 1
            

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
        else:
            break

    #close files / connections
    conn.commit()
    conn.close()

##d.)
def fileCreateTables(infile):
    '''creates a table loaded from the text file day of tweets'''

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
text VarChar2(450),
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
    FD = open(infile,'r')
    
    #load table / counter & tweet requirement
    geoID = 1
    counter = 0
    #for loop to read tweets
    for tweet in FD:
        
        #check for error tweets and append to error file
        try:
            tdict = json.loads(tweet)
        except ValueError:
            continue
        #load user/tweet data into a list before inserting
        if tdict['geo'] == None:
            
            userData = [tdict['user']['id'], tdict['user']['name'], tdict['user']['screen_name'],
                        tdict['user']['description'], tdict['user']['friends_count']]

            tweetData = [tdict['created_at'], tdict['id_str'], tdict['text'],
                        tdict['source'], tdict['in_reply_to_user_id'],
                        tdict['in_reply_to_screen_name'], tdict['in_reply_to_status_id'],
                        tdict['retweet_count'], tdict['contributors'], tdict['user']['id'],
                         None]
        else:
            userData = [tdict['user']['id'], tdict['user']['name'], tdict['user']['screen_name'],
                        tdict['user']['description'], tdict['user']['friends_count']]

            tweetData = [tdict['created_at'], tdict['id_str'], tdict['text'],
                        tdict['source'], tdict['in_reply_to_user_id'],
                        tdict['in_reply_to_screen_name'], tdict['in_reply_to_status_id'],
                        tdict['retweet_count'], tdict['contributors'], tdict['user']['id'],
                         geoID]
            geoData = [geoID, tdict['geo']['type'], tdict['geo']['coordinates'][0],
                       tdict['geo']['coordinates'][1]]
            cursor.execute('Insert or Ignore into geo values (?, ?, ?, ?);', geoData)
            geoID += 1
        

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
    FD.close()

##e.)
def executeMany(infile):
    '''creates a table loaded from the text file day of tweets'''

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
text VarChar2(450),
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
    FD = open(infile,'r')
    content = FD.read().split('\n')

    #delete unecessary rows in list
    content = listDel(content, '')
    
    #load table / counter & tweet requirement
    geoID = 1
    tweetBatch = []
    userBatch = []
    geoBatch = []
    

    #execute batch for user/geo/tweet
    for tweet in content:
        try:
            tdict = json.loads(tweet)
        except:
            continue
        if tdict['geo'] == None:
            userBatch.append([tdict['user']['id'], tdict['user']['name'], tdict['user']['screen_name'],
                        tdict['user']['description'], tdict['user']['friends_count']])
            tweetBatch.append([tdict['created_at'], tdict['id_str'], tdict['text'],
                        tdict['source'], tdict['in_reply_to_user_id'],
                        tdict['in_reply_to_screen_name'], tdict['in_reply_to_status_id'],
                        tdict['retweet_count'], tdict['contributors'], tdict['user']['id'],
                         None])
        else:
            userBatch.append([tdict['user']['id'], tdict['user']['name'], tdict['user']['screen_name'],
                        tdict['user']['description'], tdict['user']['friends_count']])
            geoBatch.append([geoID, tdict['geo']['type'], tdict['geo']['coordinates'][0],
                       tdict['geo']['coordinates'][1]])
            tweetBatch.append([tdict['created_at'], tdict['id_str'], tdict['text'],
                        tdict['source'], tdict['in_reply_to_user_id'],
                        tdict['in_reply_to_screen_name'], tdict['in_reply_to_status_id'],
                        tdict['retweet_count'], tdict['contributors'], tdict['user']['id'],
                         geoID])
            geoID += 1
            #check for geo batch
            if len(geoBatch) >= 250:
                cursor.executemany('Insert or Ignore into geo values (?, ?, ?, ?);', geoBatch)
                geoBatch = []
            #check for user batch
            if len(userBatch) >= 3000:
                cursor.executemany('Insert or Ignore into users values (?, ?, ?, ?, ?);',userBatch)
                userBatch = []
            #check for tweet batch
            if len(tweetBatch) >= 3000:
                cursor.executemany('Insert or Ignore into tweets values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', tweetBatch)
                tweetBatch = []
                
    #execute remainder of the rows
    cursor.executemany('Insert or Ignore into geo values (?, ?, ?, ?);', geoBatch)
    cursor.executemany('Insert or Ignore into users values (?, ?, ?, ?, ?);',userBatch)
    cursor.executemany('Insert or Ignore into tweets values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', tweetBatch)

    #close/commit files
    conn.commit()
    conn.close()
    FD.close()

def listDel(lst,value):
    '''deletes all of an item from a given list'''
    res = []
    for i in lst:
        if i != value:
            res.append(i)
    return res

##f.)
def plotTimes():
    '''plots the run times for questions a) - e)'''

    #initialize tweet counts
    tweetCount1 = 60000
    tweetCount2 = 600000
    #partA
    aStart = time.time()
    downloadTweets('60ktweets.txt',tweetCount1)
    aEnd = time.time()
    aTime1 = aEnd - aStart

    aStart = time.time()
    downloadTweets('600ktweets.txt',tweetCount2)
    aEnd = time.time()
    aTime2 = aEnd - aStart
    
    #partC
    cStart = time.time()
    webCreateTables(tweetCount1)
    cEnd = time.time()
    cTime1 = cEnd - cStart

    cStart = time.time()
    webCreateTables(tweetCount2)
    cEnd = time.time()
    cTime2 = cEnd - cStart

    #partD
    dStart = time.time()
    fileCreateTables('60ktweets.txt')
    dEnd = time.time()
    dTime1 = dEnd - dStart

    dStart = time.time()
    fileCreateTables('600ktweets.txt')
    dEnd = time.time()
    dTime2 = dEnd - dStart

    #partE
    eStart = time.time()
    executeMany('60ktweets.txt')
    eEnd = time.time()
    eTime1 = eEnd - eStart

    eStart = time.time()
    executeMany('600ktweets.txt')
    eEnd = time.time()
    eTime2 = eEnd - eStart
    
    #plot times
    fig = plt.figure()
    sp1 = fig.add_subplot(1,1,1)
    sp1.scatter(tweetCount1, aTime1)
    sp1.scatter(tweetCount2, aTime2)
    sp1.scatter(tweetCount1, cTime1)
    sp1.scatter(tweetCount2, cTime2)
    sp1.scatter(tweetCount1, dTime1)
    sp1.scatter(tweetCount2, dTime2)
    sp1.scatter(tweetCount1, eTime1)
    sp1.scatter(tweetCount2, eTime2)

    #label points, axis, title
    plt.annotate("Part A",xy=(60000,aTime1))
    plt.annotate("Part A",xy=(600000,aTime2))
    plt.annotate("Part C",xy=(60000,cTime1))
    plt.annotate("Part C",xy=(600000,cTime2))
    plt.annotate("Part D",xy=(60000,dTime1))
    plt.annotate("Part D",xy=(600000,dTime2))
    plt.annotate("Part E",xy=(60000,eTime1))
    plt.annotate("Part E",xy=(600000,eTime2))
    plt.xlabel('# of Tweets')
    plt.ylabel('Time to Execute')
    plt.title('Tweet Count versus Execution Time Part A, C, D, E')
    plt.show()

#Part 2

##a.)
def sqlQuery():
    '''finds the min lat/long for each user from the db'''

    #connect to db
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()

    #write query
    query = '''select tweets.user_id, min(geo.longitude), min(geo.latitude) from tweets
inner join geo on tweets.geo_id = geo.id group by tweets.user_id;'''

    #run query
    
    return cursor.execute(query).fetchall()

##b.)
def multipleQueries():
    '''runs part 2a code 10 and 100 times to see if execution time scales linearly'''

    #start time
    start = time.time()

    #for loop
    for i in range(10):
        sqlQuery()

    #end time
    end = time.time()
    totalTime1 = end - start

    #start time
    start = time.time()

    #for loop
    for i in range(100):
        sqlQuery()

    #end time
    end = time.time()
    totalTime2 = end - start

    print(f'Running the query 10 times took {totalTime1} seconds')
    print(f'Running the query 100 times took {totalTime2} seconds')

##c.)
def textQuery(file):
    '''same query as part a.) without using the database'''

    #open file, store data in list, close file
    infile = open(file,'r')
    content = infile.read().split('\n')
    content = listDel(content,'')
    infile.close()

    #create resulting list, run for loop
    res = {}
    for tweet in content:
        try:
            
            tdict = json.loads(tweet)
        except:
            continue
        if tdict['geo'] == None:
            continue
        if tdict['user']['id'] in res.keys():
            if tdict['geo']['coordinates'][0] < res[tdict['user']['id']][0]:
                res[tdict['user']['id']][0] = tdict['geo']['coordinates'][0]
            elif tdict['geo']['coordinates'][1] < res[tdict['user']['id']][1]:
                res[tdict['user']['id']][1] = tdict['geo']['coordinates'][1]
        else:
            res[tdict['user']['id']] = [tdict['geo']['coordinates'][0],tdict['geo']['coordinates'][1]]

    return res

##d.)
def textQueries():
    '''runs part 2c code 10 and 100 times to see if execution time scales linearly'''

    #start time
    start = time.time()

    #for loop
    for i in range(10):
        textQuery('600ktweets.txt')

    #end time
    end = time.time()
    totalTime1 = end - start

    #start time
    start = time.time()

    #for loop
    for i in range(100):
        textQuery('600ktweets.txt')

    #end time
    end = time.time()
    totalTime2 = end - start

    print(f'Running the query 10 times took {totalTime1} seconds')
    print(f'Running the query 100 times took {totalTime2} seconds')

##e.)
def expQuery(file):
    '''same query as part c.) but using reg exp instead of json.loads'''

    #open file, store data in list, close file
    infile = open(file,'r')
    content = infile.read().split('\n')
    content = listDel(content,'')
    infile.close()

    #regular expressions

    ##find coordinates
    regex1 = re.compile('"coordinates":\[.*?\]')
    regex2 = re.compile(':\[.*?\]')
    ##find user
    regex3 = re.compile('"user":{"id":\d\d\d\d\d\d\d')
    res = {}   
    for tweet in content:
        e1 = re.findall(regex1,tweet)
        e2 = re.findall(regex3,tweet)

        if e1 == []:
            continue
        else:
            e1 = re.findall(regex2,e1[0])
            e1 = e1[0][2:-1].split(',')
            try:
                
                e2 = e2[0][13:-1]
            except:
                continue
            if e2 in res.keys():
                if res[e2][0] > e1[0]:
                    res[e2][0] = e1[0]
                if res[e2][1] > e1[1]:
                    res[e2][1] = e1[1]
            else:
                res[e2] = e1

    return res
        
        
##f.)
def expQueries():
    '''runs part 2c code 10 and 100 times to see if execution time scales linearly'''

    #start time
    start = time.time()

    #for loop
    for i in range(10):
        expQuery('600ktweets.txt')

    #end time
    end = time.time()
    totalTime1 = end - start

    #start time
    start = time.time()

    #for loop
    for i in range(100):
        expQuery('600ktweets.txt')

    #end time
    end = time.time()
    totalTime2 = end - start

    print(f'Running the query 10 times took {totalTime1} seconds')
    print(f'Running the query 100 times took {totalTime2} seconds')

#Part 3

##a.)

def newTable():
    '''creates a table by joining all 3 tables in the db'''

    #sqlite3 connection
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()

    #query
    query = '''create table newTable as
select tweets.created_at, tweets.id_str, tweets.text,
tweets.source, tweets.in_reply_to_user_id, tweets.in_reply_to_screen_name,
tweets.in_reply_to_status_id, tweets.retweet_count, tweets.contributors,
tweets.user_id, tweets.geo_id, geo.type, geo.longitude, geo.latitude,
users.name, users.screen_name, users.description, users.friends_count
from tweets
left outer join geo on (tweets.geo_id = geo.id)
left outer join users on (tweets.user_id = users.id);'''

    #drop table if already created, otherwise create table
    try:
        cursor.execute(f'drop table newTable')
    except:
        pass
    cursor.execute(query)

    #close/commit files
    conn.commit()
    conn.close()

##b.)
def exportToJson():
    '''takes the newly created table and puts it into a json file'''

    #sqlite3 connection
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()
    d = {'created_at':[],'id_str':[],'text':[],'source':[],
         'in_reply_to_user_id':[],'in_reply_to_screen_name':[],
         'in_reply_to_status_id':[],'retweet_count':[],'contributors':[],
         'user_id':[],'geo_id':[], 'type':[], 'longitude':[],'latitude':[],
         'name':[], 'screen_name':[],'description':[], 'friends_count':[]}
    #load query into dict
    cursor.execute('select * from newTable;')
    for i in cursor:
        d['created_at'].append(i[0])
        d['id_str'].append(i[1])
        d['text'].append(i[2])
        d['source'].append(i[3])
        d['in_reply_to_user_id'].append(i[4])
        d['in_reply_to_screen_name'].append(i[5])
        d['in_reply_to_status_id'].append(i[6])
        d['retweet_count'].append(i[7])
        d['contributors'].append(i[8])
        d['user_id'].append(i[9])
        d['geo_id'].append(i[10])
        d['type'].append(i[11])
        d['longitude'].append(i[12])
        d['latitude'].append(i[13])
        d['name'].append(i[14])
        d['screen_name'].append(i[15])
        d['description'].append(i[16])
        d['friends_count'].append(i[17])
        

    #json dump
    json_object = json.dumps(d, indent=4)

    #open json file, write to it
    outfile = open('Sample_Json.json','w')
    outfile.write(json_object)

    #close/commit files
    outfile.close()
    conn.commit()
    conn.close()

##c.)
def exportToCSV():
    '''takes newly created table and exports to csv file'''
    
        #sqlite3 connection
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()
    l = []
    #load query into list
    cursor.execute('select * from newTable;')
    for i in cursor:
        i = list(i)
        i = ['None' if v is None else v for v in i]
        i = [str(v) if type(v) == int or type(v) == float else v for v in i]
               
        l.append(i[0]+' ,'+i[1]+' ,'+i[2]+' ,'+i[3]+' ,'+i[4]+' ,'+i[5]
                    +' ,'+i[6]+' ,'+i[7]+' ,'+i[8]+' ,'+i[9]+' ,'+i[10]+' ,'+i[11]
                    +' ,'+i[12]+' ,'+i[13]+' ,'+i[14]+' ,'+i[15]+' ,'+i[16]
                    +' ,'+i[17]+'\n')

    #open csv file, write to it
    outfile = open('sample_csv.csv','w')

    for lst in l:
        outfile.write(lst)
            
    #close/commit files
    outfile.close()
    conn.commit()
    conn.close()
    
