import csv, sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE Events (Adate, year, annotation, event, source, url);") # use your column names here

with open('Syriantimeline.csv','rt') as fin: # `with` statement available in 2.5+ (data.csv is the data file)
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Date'], i['Year'], i['Annotation'], i['Event'], i['Source'], i['Source URL']) for i in dr]

cur.executemany("INSERT INTO Events (Adate, year, annotation, event, source, url) VALUES (?, ?, ?, ?, ?, ?);", to_db)
con.commit()
#add code to create a column for severity
con.close()
