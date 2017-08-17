import mysql.connector
import time
import untangle
import dbconnect
import ebaycheck
import comic

cfg = dict(user='bill', password='gojets', host='localhost', database='comicbooks', raise_on_warnings=True)

add_comic = ("INSERT INTO comics "
             "(Title, Number, Publisher, Date) "
             "VALUES (%(Title)s, %(Number)s, %(Publisher)s, %(Date)s)")
add_price = ("INSERT INTO prices "
             "(ComicID, Price, URL, LastUpdate) "
             "VALUES (%(ComicID)s, %(Price)s, %(URL)s, %(LastUpdate)s)")

win_path = "C:\Dev\pricechecker\comics.xml"
linux_path = "/home/bill/dev/Crossroads/comics.xml"

NUM_RESULTS = 10 #number of results to store for each comic

def update_prices(config):
    cfg = config
    database = dbconnect.DB(cfg)
    cursor = database.csr

class PriceList:
    def __init__(self, config):
        self.config = config


    def update_prices(self):
        self.database = dbconnect.DB(self.config)
        self.cursor = self.database.cnx.cursor(buffered=True)
        self.database.initialize_tables()
        i = 0
        data_price = {}
        try:
            self.cursor.execute("SELECT * FROM comics")
        except mysql.connector.Error as err:
            print("Bad SQL dude")
            print(err)
        for book in self.cursor.fetchall():
            t = book[1] + " " + str(book[2])
            pupdate = ebaycheck.SearchResults(t, NUM_RESULTS)
            print("Updating price for %s #%s" % (book[1], book[2]))
            prices = pupdate.query()
            data_price['ComicID'] = book[0]
            i = 0
            for price in prices:
                try:
                    data_price['Price'] = price.sellingStatus.currentPrice.value
                except AssertionError as e:
                    data_price['Price'] = -1
                    print(e)
                try:
                    data_price['URL'] = price.viewItemURL
                except AssertionError as e:
                    data_price['URL'] = 'NA'
                    print(e)
                data_price['LastUpdate'] = time.strftime("%Y/%m/%d")
                print("Adding price of %s" % data_price['Price'])
                self.cursor.execute(add_price, data_price)
                i = i + 1
                if i > 100:
                    self.database.cnx.commit()
                    print("Committing...")
                    i = 0
            self.database.cnx.commit()
        return (self.cursor)


class XMLImport:
    def __init__(self, importfilepath):
        self.XML = importfilepath
        try:
            self.file = untangle.parse(self.XML)
        except (SyntaxError, IOError):
            print("Error importing - check your filename/path")


    def import_comics(self, config=cfg):
        self.config = config
        self.database = dbconnect.DB(self.config)
        self.cursor = self.database.cnx.cursor(buffered=True)
        self.database.initialize_tables()
        i = 0
        data_comic = {}
        for issue in self.file.comicinfo.comiclist.comic:
           #number check
            try:
                num = issue.mainsection.issuenr.cdata
            except AttributeError:
                num = 0

            #date check
            try:
                dt = issue.releasedate.date.cdata
            except AttributeError:
                dt = 'NA'
            floppy = comic.Comic(title=issue.mainsection.series.displayname.cdata,
                                 number=num,
                                 publisher=issue.publisher.displayname.cdata,
                                 date=dt)
            floppy.dbInsert(config=config)
            print("Adding comic %s number %s" % (floppy.title, floppy.num))
            i = i+1
            if i > 100:
                self.database.cnx.commit()
                print("Committing...")
                i = 0
        self.database.cnx.commit()
        print("Final commit...")
        return(self.cursor)

if __name__ == '__main__':
    file = raw_input('Enter XML import file:')
    if file == '':
        porty = XMLImport(win_path)
    else:
        porty = XMLImport(file)
    porty.import_comics()
    pricecheck = raw_input('Check prices? (Y/N)')
    if pricecheck == 'Y' or pricecheck == 'y':
        list = PriceList(cfg)
        list.update_prices()
    else:
        print('Skipping price check this time...')






