import csv, sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE t (searchid, publication, Adate, title, edition, journal, pubtype, highlight, byline, lang, section, load, length, aText);") # use your column names here

with open('nexistestdata.csv','rt') as fin: # `with` statement available in 2.5+ (data.csv is the data file)
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    print(dr)
    wait = input("PRESS ENTER TO CONTINUE.")
    to_db = [(i['SEARCH_ID'], i['PUBLICATION'], i['ADATE'], i['TITLE'], i['EDITION'], i['JOURNAL-CODE'], i['PUBLICATION-TYPE'], i['HIGHLIGHT'], i['BYLINE'], i['LANGUAGE'], i['SECTION'], i['LOAD-DATE'], i['LENGTH'], i['TEXT']) for i in dr]

cur.executemany("INSERT INTO t (searchid, publication, Adate, title, edition, journal, pubtype, highlight, byline, lang, section, load, length, aText) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()

