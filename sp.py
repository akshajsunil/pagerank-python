
import sqlite3


conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS Pages''')
