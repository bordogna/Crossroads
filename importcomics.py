import mysql.connector
from mysql.connector import errorcode
import untangle
import dbconnect
import ebaycheck

add_comic = ("INSERT INTO comics "
             "(Title, Number, Publisher, Date) "
             "VALUES (%(Title)s, %(Number)s, %(Publisher)s, %(Date)s)")
add_price = ("INSERT INTO prices "
             "(PriceID, ComicID, Price, LastUpdate) "
             "VALUES (%(PriceID)s, %(ComicID)s, %(Price)s, %(LastUpdate)s)")

def update_prices(config):
    cfg = config
    cnx = dbconnect.create_connection(cfg)
    cursor = cnx.cursor(buffered=True)
    i = 0
    data_price = {}
    print(cursor.execute("SELECT * FROM comics WHERE Number=1"))
    try:
        comicsToUpdate = cursor.execute("SELECT * FROM comics WHERE Number=1")
    except mysql.connector.Error as err:
        print("Bad SQL dude")
        print(err)
    for book in comicsToUpdate.fetchall():
        pupdate = ebaycheck.Searcher(book.Title, 'Yes')
        print("Updating price for %s #%s" % (book.Title, book.Number))
        prices = pupdate.query()
        data_price['ComicID'] = book.ComicID
        for price in prices:
            try:
                data_price['Price'] = price.sellingStatus.currentPrice.value
            except AssertionError:
                data_price['Price'] = -1
            data_price['LastUpdate'] = time.strftime("%Y/%m/%d")
            print("Adding price of " % s, data_price['Price'])
            cursor.execute(add_price, data_price)
            i = i + 1
            if i > 100:
                cnx.commit()
                print("Committing...")
                i = 0
        return (cursor)

class XMLImport:
    def __init__(self, importfilepath):
        self.XML = importfilepath
        try:
            self.file = untangle.parse(self.XML)
        except (SyntaxError, IOError):
            print("Error importing - check your filename/path")


    def import_comics(self, config):
        self.config = config
        cnx = dbconnect.create_connection(self.config)
        cursor = cnx.cursor()
        i = 0
        data_comic = {}
        for issue in self.file.comicinfo.comiclist.comic:
            #build out comic SQL
            data_comic['Title'] = issue.mainsection.series.displayname.cdata
           #number check
            try:
                num = issue.mainsection.issuenr.cdata
            except AttributeError:
                num = 0
            data_comic['Number'] = num
            data_comic['Publisher'] = issue.publisher.displayname.cdata
            #date check
            try:
                dt = issue.releasedate.date.cdata
            except AttributeError:
                dt = 'NA'
            data_comic['Date'] = dt
            print('Adding comic %s number %s', data_comic['Title'], data_comic['Number'])
            cursor.execute(add_comic, data_comic)
            i = i+1
            if i > 100:
                cnx.commit()
                print("Committing...")
                i = 0
        return(cursor)







