createtbl = """
CREATE TABLE Animal
(
  AID       NUMBER(3, 0),
  AName      VARCHAR2(30) NOT NULL,
  ACategory VARCHAR2(18),

  TimeToFeed NUMBER(4,2),

  CONSTRAINT Animal_PK
    PRIMARY KEY(AID)
);
"""

inserts = ["INSERT INTO Animal VALUES(1, 'Galapagos Penguin', 'exotic', 0.5);", "INSERT INTO Animal VALUES(2, 'Emperor Penguin', 'rare', 0.75);", "INSERT INTO Animal VALUES(3, 'Sri Lankan sloth bear', 'exotic', 2.5);", "INSERT INTO Animal VALUES(4, 'Grizzly bear', 'common', 3.0);", "INSERT INTO Animal VALUES(5, 'Giant Panda bear', 'exotic', 1.5);", "INSERT INTO Animal VALUES(6, 'Florida black bear', 'rare', 1.75);", "INSERT INTO Animal VALUES(7, 'Siberian tiger', 'rare', 3.25);", "INSERT INTO Animal VALUES(8, 'Bengal tiger', 'common', 2.75);", "INSERT INTO Animal VALUES(9, 'South China tiger', 'exotic', 2.5);", "INSERT INTO Animal VALUES(10, 'Alpaca', 'common', 0.25);", "INSERT INTO Animal VALUES(11, 'Llama', NULL, 3.5);"]

import sqlite3

conn = sqlite3.connect('dsc450.db') # open the connection
cursor = conn.cursor()

cursor.execute(createtbl)   # create the Animal table
for ins in inserts:         # insert the rows
    cursor.execute(ins)

conn.commit()   # finalize inserted data
conn.close()    # close the connection

createtb2 = """
CREATE TABLE Animal2
(
  AID       NUMBER(3, 0),
  AName      VARCHAR2(30) NOT NULL,
  ACategory VARCHAR2(18),

  TimeToFeed NUMBER(4,2),

  CONSTRAINT Animal2_PK
    PRIMARY KEY(AID)
);
"""
