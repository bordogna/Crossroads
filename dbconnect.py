from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode

config = dict(user='bill', password='gojets', host='localhost', database='comicbooks', raise_on_warnings=True)
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
    "  `ComicID` int(32) NOT NULL UNIQUE AUTO_INCREMENT,"
    "  `Title` varchar(255) NOT NULL,"
    "  `Number` int(32) NOT NULL DEFAULT 0,"
    "  `Publisher` varchar(255),"
    "  `Date` varchar(255),"
    "  PRIMARY KEY (`ComicID`),"
    "  UNIQUE KEY `unique_comic` (`Title`,`Number`,`Date`)"
    ") ENGINE=InnoDB")

TABLES['prices'] = (
    "CREATE TABLE IF NOT EXISTS `prices` ("
    "  `PriceID` int(32) NOT NULL AUTO_INCREMENT,"
    "  `ComicID` int(32) NOT NULL,"
    "  `Price` DECIMAL(10,2),"
    "  `URL` varchar(255),"
    "  `LastUpdate` date,"
    "  `Verified` bool,"
    "  PRIMARY KEY (`PriceID`)"
    ") ENGINE=InnoDB")

class DB:
    def __init__(self, config):
        self.config = config
        try:
            self.cnx = mysql.connector.connect(**config)
            self.csr = self.cnx.cursor(buffered=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist - creating it now")
                create_database(self.csr)
            else:
                print(err)

    def create_database(self):
        try:
            self.csr.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def initialize_tables(self):
        initial = DB(config)
        for name, ddl in TABLES.iteritems():
            try:
                print("Creating table {}: ".format(name), end='')
                initial.csr.execute(ddl)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

