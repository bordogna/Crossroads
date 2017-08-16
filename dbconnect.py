from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode

config = dict(user='bill', password='gojets', host='127.0.0.1', database='comicbooks', raise_on_warnings=True)
DB_NAME = 'comicbooks'

TABLES = {}

TABLES['users'] = (
    "CREATE TABLE IF NOT EXISTS `users` ("
    "  `UserID` int(32) NOT NULL AUTO_INCREMENT,"
    "  `First` varchar(255) NOT NULL,"
    "  `Last` varchar(255) NOT NULL,"
    "  `Password` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`UserID`)"
    ") ENGINE=InnoDB")

TABLES['comics'] = (
    "CREATE TABLE IF NOT EXISTS `comics` ("
    #"  `UserID` int(32) NOT NULL,"
    "  `ComicID` int(32) NOT NULL AUTO_INCREMENT,"
    "  `Title` varchar(255) NOT NULL,"
    "  `Number` int(32) NOT NULL DEFAULT 0,"
    "  `Publisher` varchar(255),"
    "  `Date` varchar(255),"
    "  PRIMARY KEY (`ComicID`)"
    ") ENGINE=InnoDB")

TABLES['prices'] = (
    "CREATE TABLE IF NOT EXISTS `prices` ("
    "  `PriceID` int(32) NOT NULL AUTO_INCREMENT,"
    "  `ComicID` int(32) NOT NULL,"
    "  `Price` numeric(32),"
    "  `LastUpdate` date,"
    "  PRIMARY KEY (PriceID), KEY `comic` (`ComicID`)"
    ") ENGINE=InnoDB")

def create_connection(config):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        return (cnx)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist - creating it now")
        else:
            print(err)

def close_connection(cnx):
    cnx.close()


cnx = mysql.connector.connect(user='bill', password='gojets')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


try:
    cnx.database = DB_NAME
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

# for name, ddl in TABLES.iteritems():
#     try:
#         print("Creating table {}: ".format(name), end='')
#         cursor.execute(ddl)
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#             print("already exists.")
#         else:
#             print(err.msg)
#     else:
#         print("OK")

cursor.close()
cnx.close()