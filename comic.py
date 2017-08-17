import time
import dbconnect
import ebaycheck
import mysql.connector

config = dict(user='bill', password='gojets', host='localhost', database='comicbooks', raise_on_warnings=True)

add_comic = ("INSERT INTO comics "
             "(Title, Number, Publisher, Date) "
             "VALUES (%(Title)s, %(Number)s, %(Publisher)s, %(Date)s)")
add_price = ("INSERT INTO prices "
             "(ComicID, Price, URL, LastUpdate) "
             "VALUES (%(ComicID)s, %(Price)s, %(URL)s, %(LastUpdate)s)")

class Comic:
    def __init__(self, title, number=0, publisher='NA', date=time.strftime("%Y/%m/%d")):
        self.title = title
        self.num = number
        self.pub = publisher
        self.date = date

    def dbInsert(self, config):
        data_comic = {}
        db = dbconnect.DB(config)
        # build out comic SQL
        data_comic['Title'] = self.title
        data_comic['Number'] = self.num
        data_comic['Publisher'] = self.pub
        data_comic['Date'] = self.date
        try:
            print("Adding comic %s number %s" % (data_comic['Title'], data_comic['Number']))
            db.csr.execute(add_comic, data_comic)
            db.csr.execute("SELECT LAST_INSERT_ID();")
            dbrecord = db.csr.fetchall()
            self.comicid = dbrecord[0]
            db.cnx.commit()
        except mysql.connector.Error as err:
            print(err)

    def updatePrice(self, config):
        data_price = {}
        db = dbconnect.DB(config)
        if self.comicid != '':
            data_price['ComicID'] = self.comicid
        else:
            db.csr.execute("SELECT * FROM comics WHERE Title=%s AND Number=%s AND Date=%s" % (self.title, self.num, self.date))
            dbrecord = db.csr.fetchall()
            self.comicid = dbrecord[0]
            data_price['ComicID'] = self.comicid
        t = self.title + " #" + str(self.num)
        pupdate = ebaycheck.Searcher(t)
        print("Updating price for %s #%s" % (book[1], book[2]))
        prices = pupdate.query()
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
            db.csr.execute(add_price, data_price)
            db.cnx.commit()