import csv, sqlite3

con = sqlite3.connect("EventsTimeline.db")
cur = con.cursor()
cur.execute("CREATE TABLE Events (Date, EventText, Average, Mode);") 

with open('EventsFinal.csv','rt') as fin: # `with` statement available in 2.5+ (data.csv is the data file)
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Date'], i['EventText'], i['Average'], i['Mode']) for i in dr]

cur.executemany("INSERT INTO Events (Date, EventText, Average, Mode) VALUES (?, ?, ?, ?);", to_db)
con.commit()
#add code to create a column for severity

cur.execute('SELECT * FROM Events group by Mode')
rows = cur.fetchall()

for row in rows:
    print(row)

con.close()
