import csv, sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE Events (date, year, annot, event, source, url, severity);") # use your column names here


with open('data.csv','rb') as fin: # `with` statement available in 2.5+ (data.csv is the data file)
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['data'], i['year'], i['annot'], i['event'], i[source], i[url], i[severity]]) for i in dr]

cur.executemany("INSERT INTO t (date, year, annot, event, source, url, severity) VALUES ((?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()
