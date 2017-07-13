import csv, sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE t (searchid, pub, date, title, edition, journal, pubtype, highlight, byline, lang, section, load, length, Text);") # use your column names here


with open('data.csv','rb') as fin: # `with` statement available in 2.5+ (data.csv is the data file)
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['searchid'], i['pub'], i['title'], i['edition'], i[journal], i[pubtype], i[highlight], i[byline], i[lang], i[section], i[load], i[length], i[Text]) for i in dr]

cur.executemany("INSERT INTO t (searchid, pub, date, title, edition, journal, pubtype, highlight, byline, lang, section, load, length, Text) VALUES ((?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()

