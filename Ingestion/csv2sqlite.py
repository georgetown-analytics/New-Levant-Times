import csv, sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE t (searchid, pub, date, title, edition);") # use your column names here


with open('data.csv','rb') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['searchid'], i['pub'], i['title'], i['edition']) for i in dr]

cur.executemany("INSERT INTO t (searchid, pub, date, title, edition) VALUES ((?, ?, ?, ?);", to_db)
con.commit()
con.close()

