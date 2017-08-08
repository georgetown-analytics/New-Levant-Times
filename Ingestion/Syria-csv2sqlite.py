import csv, sqlite3

con = sqlite3.connect("SyriaText.db")
cur = con.cursor()
cur.execute("CREATE TABLE t (publication, date, title, length, publicationtype, text, year, month, day);") # use your column names here

with open('CleanLexisNexis.csv','rt') as fin: # `with` statement available in 2.5+ (data.csv is the data file)
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
   
   # wait = input("PRESS ENTER TO CONTINUE.")
    to_db = [(i['publication'], i['date'], i['title'], i['length'], i['publicationtype'], i['text'], i['year'], i['month'], i['day']) for i in dr]

cur.executemany("INSERT INTO t (publication, date, title, length, publicationtype, text, year, month, day) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()

cur.execute('SELECT * FROM t group by Publication')
rows = cur.fetchall()
 
for row in rows:
    print(row)

con.close()

