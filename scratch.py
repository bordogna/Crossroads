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

importPathLinux = '/home/bill/Dev/Crossroads/comics.xml'
importPathWin = 'C:\Dev\Crossroads\comics.xml'

config = dict(user='bill', password='gojets', host='127.0.0.1', database='comicbooks', raise_on_warnings=True)
#Load in comics from xml
#cmx = importcomics.XMLImport(importPathLinux)
#cursor = cmx.import_comics(config)

#refresh prices from eBay
pl = importcomics.PriceList(config)
pl.update_prices()







