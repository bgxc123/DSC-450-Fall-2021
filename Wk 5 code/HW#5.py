#Name: Brendan
#Date: 10/17/21
#Assignment: DSC450
import sqlite3
import csv
import json
def chauffeurDataLoad(infile):
    '''takes in the chauffeur csv file and inserts the data into sqlite'''

    #set connection
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()
    chauffeurTable = '''create table chauffeur (
License_Number Number(6),
Renewed Date,
Status VarChar2(20),
Status_Date Date,
Driver_Type VarChar2(20),
License_Type VarChar2(20),
Original_Issue_Date Date,
Name VarChar2(100),
Sex VarChar2(6),
Chauffeur_City VarChar2(50),
Chauffeur_State Char(2),
Record_Number Char(11),

Constraint Chauffeur_PK
Primary Key (Record_Number)
);'''
    #drop table if exists, otherwise create
    try:
        cursor.execute(f'Drop table chauffeur;')
    except:
        pass
    cursor.execute(chauffeurTable)

    #open csv file using csvreader
    fd = open('Public_Chauffeurs_Short_hw3.csv', 'r')
    reader = csv.reader(fd)
    header = []
    header = next(reader)

    rows = []
    for row in reader:
        rows.append(row)

    #insert values into db
    for row in rows:
        for j in range(len(row)):
            if row[j] == 'NULL' or row[j] =='':
                row[j] = None
        cursor.execute(f'Insert or Ignore into Chauffeur values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', row)

    #close file & db conn
    conn.commit()
    conn.close()
    fd.close()


def tweetReader(infile):
    '''takes in a file and creates a SQL table based on 200 tweets'''

    #sqlite connection
    conn = sqlite3.connect('dsc450.db')
    cursor = conn.cursor()

    #create table if exists, drop otherwise
    tweetsTable = '''create table Tweets (
created_at Date,
id_str Char(18),
text VarChar2(280),
source VarChar2(200),
in_reply_to_user_id VarChar2(20),
in_reply_to_screen_name VarChar2(50),
in_reply_to_status_id Char(18),
retweet_count Number,
contributors VarChar2(50)

);'''
    try:
        cursor.execute(f'drop table Tweets;')
    except:
        pass
    cursor.execute(tweetsTable)

    #read in the file
    FD = open(infile, 'r')
    content = FD.read().split('EndOfTweet')

    #utilize json loads for inserting data
    res = []
    for tweet in content:
        tweet = json.loads(tweet)
        res.append([tweet['created_at'], tweet['id_str'], tweet['text'],
                    tweet['source'], tweet['in_reply_to_user_id'],
                    tweet['in_reply_to_screen_name'], tweet['in_reply_to_status_id'],
                    tweet['retweet_count'], tweet['contributors']])

    #insert data into tweets table
    for lst in res:
        for j in range(len(lst)):
            if lst[j] == '' or lst[j] == 'NULL':
                lst[j] = None
        cursor.execute('Insert into Tweets values (?, ?, ?, ?, ?, ?, ?, ?, ?);', lst)

    #close files / connections
    conn.commit()
    conn.close()
    FD.close()
        
    
        

    
    
    
    
