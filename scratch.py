# from passlib.hash import pbkdf2_sha256
# from passlib.hash import pbkdf2_sha256
#
# hash = pbkdf2_sha256.encrypt("gojets", rounds=20000, salt_size=16)
#
# print(pbkdf2_sha256.verify("gojets", hash))

#a = Searcher("here's negan", 'No')
#a.query()
from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
import dbconnect
import ebaycheck
import importcomics

config = dict(user='bill', password='gojets', host='127.0.0.1', database='comicbooks', raise_on_warnings=True)
pl = importcomics.PriceList(config)
pl.update_prices()
# cmx = importcomics.XMLImport('C:\Dev\pricechecker\comics.xml')
# curseor = cmx.import_comics(config)
# config = dict(user='bill', password='gojets', host='127.0.0.1', database='comics', raise_on_warnings=True)
# stmt = (
#     "SELECT * FROM comics WHERE Number=1"
# )
# database = dbconnect.DB(config)
# cursor = database.csr
# list = cursor.execute(stmt)
# print(list)
# print("THE END")




