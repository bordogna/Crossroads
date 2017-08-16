import mysql.connector
from mysql.connector import errorcode
import untangle
import dbconnect

add_comic = ("INSERT INTO comics "
             "(Title, Number, Publisher, Date) "
             "VALUES (%s, %s, %s, %s, %s)")

class CSVImport:
    def __init__(self, importfilepath):
        self.path = importfilepath
        try:
            self.file = untangle.parse(importfilepath)
        except (SyntaxError, IOError):
            print("Error importing - check your filename/path")
        try:


    def run_import(self, config):
        self.config = config
        cnx = dbconnect.create_connection(self.config)
        cursor = cnx.cursor()
        for i in self.file.comiclist.comic:
            data_comic = {
                'Title' = i.mainsection.series.displayname
                'Number' = i.mainsection.issuenr
                'Publisher' = i.publisher.displayname
                'Date' = i.publicationdate.date
             }
            print('Adding comic %s #%s', data_comic['Title'], data_comic['Number'])
            cursor.execute(add_comic, data_comic)
            cnx.commit()


