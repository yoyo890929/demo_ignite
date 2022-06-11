from pyignite import Client

client = Client()
client.connect('127.0.0.1', 10800)

######################帳號##################
ACCOUNT_CREATE_TABLE_QUERY = '''CREATE TABLE Account (
    Name CHAR(20),
    ID CHAR(20),
    Password CHAR(20),
    Date CHAR(13),
    Place CHAR(20),
    PRIMARY KEY (Name, ID)
) WITH "affinityKey=ID"'''

client.sql(ACCOUNT_CREATE_TABLE_QUERY)

ACCOUNT_CREATE_INDEX = '''CREATE INDEX idx_account_code ON account (ID)'''

client.sql(ACCOUNT_CREATE_INDEX)
"""
ACCOUNT_INSERT_QUERY = '''INSERT INTO Account(
    Name, ID, Password, Date , Place
) VALUES (?, ?, ?, ?,?)'''

ACCOUNT_DATA = [
    ['Allen', 'A1234567', '1234567', '#','#'],
    ['Jeff', 'B1234567', '1234567', '#','#'],
    ['Ruby', 'C1234567', '1234567', '#','#'],
    ['Ken', 'D1234567', '1234567', '#','#'],
    ['John', 'E1234567', '1234567', '#','#'],
]

for row in ACCOUNT_DATA:
    client.sql(ACCOUNT_INSERT_QUERY, query_args=row)"""
#######################################################################

#############################實連制登記資料#############################
FOOTPRINT_CREATE_TABLE_QUERY = '''CREATE TABLE Footprint (
    Name CHAR(20),
    ID CHAR(20),
    Password CHAR(20),
    Date CHAR(13),
    Place CHAR(20),
    Key INT(20),
    PRIMARY KEY (Key)
    
) WITH "affinityKey=Key"'''

client.sql(FOOTPRINT_CREATE_TABLE_QUERY)

FOOTPRINT_CREATE_INDEX = '''CREATE INDEX idx_footprint_code ON footprint (ID)'''

client.sql(FOOTPRINT_CREATE_INDEX)
"""
FOOTPRINT_INSERT_QUERY = '''INSERT INTO Footprint(
    Name, ID, Password, Date , Place,key
) VALUES (?, ?, ?, ?,?,?)'''

FOOTPRINT_DATA = [
    ['Allen', 'A1234567', '#', '2022_0606_13','A',3],
    ['Jeff', 'B1234567', '#', '2022_0606_13','A',4],
]

for row in FOOTPRINT_DATA:
    client.sql(FOOTPRINT_INSERT_QUERY, query_args=row)"""
#############################################################

########################確診者登記資料########################
CONFIRMED_CREATE_TABLE_QUERY = '''CREATE TABLE Confirmed (
    Name CHAR(20),
    ID CHAR(20),
    Password CHAR(20),
    Date CHAR(13),
    Place CHAR(20),
    Key INT(10),
    PRIMARY KEY (Key)
) WITH "affinityKey=Key"'''

client.sql(CONFIRMED_CREATE_TABLE_QUERY)

CONFIRMED_CREATE_INDEX = '''CREATE INDEX idx_confirmed_code ON confirmed (ID)'''

client.sql(CONFIRMED_CREATE_INDEX)
"""
CONFIRMED_INSERT_QUERY = '''INSERT INTO Confirmed(
    Name, ID, Password, Date , Place ,Key
) VALUES (?, ?, ?, ?,?,?)'''

CONFIRMED_DATA = [
    ['Allen', 'A1234567', '#', '2022_0606_12','A',1],
    ['Jeff', 'B1234567', '#', '2022_0606_13','A',2],
]

for row in CONFIRMED_DATA:
    client.sql(CONFIRMED_INSERT_QUERY, query_args=row)"""
#############################################################
CONFIRMED_SELECT_QUERY = "SELECT * FROM Confirmed"

confirmeds = client.sql(CONFIRMED_SELECT_QUERY)
for confirmed in confirmeds:
    print(*confirmed)

FOOTPRINT_SELECT_QUERY = "SELECT * FROM Footprint"

footprints = client.sql(FOOTPRINT_SELECT_QUERY)
for footprint in footprints:
    print(*footprint)

