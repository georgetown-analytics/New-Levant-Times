# coding: utf-8
# Generates word counts from "Event" description field in csv file output
# from SyrianTimeline_wikipedia.py: Syriantimelinefinal.csv
# Melanie Huston
# July 2017

import re
import os
import csv
from string import punctuation

rowcount = 0
statuscounter = 0
words= []
words_counted = []

# Record each word's occurrence in the event descriptions from csv file
print('Getting words...\n')
with open('Syriantimelinefinal.csv', 'r') as csvfile:
    readthing = csv.reader(csvfile)
    next(readthing) # skip header row
    for row in readthing:
        rowcount += 1
        csv_words = row[3].split(" ") # split all "words" on spaces in event description
        for i in csv_words:
            # if this "word" has letters in it, process and add to words list
            if re.search('[a-zA-Z]', i):
                # remove quotes, curly quotes and ellipses
                i = i.replace(u'\u2018', '').replace(u'\u2019', '').replace(u'\u201c', '').replace(u'\u201d', '').replace(u'\u2026', '')
                i = i.strip(punctuation)
                i = i.lower()
                words.append(i)
        # print status message for each 100 events processed
        if not rowcount % 100:
            print(rowcount, "rows processed.")
    print(rowcount, "total rows processed.\n")
csvfile.close()

# Record a count for each word in the words list
print('Recording word counts...\n')
for i in words:
    x = words.count(i)
    # if the word-and-count pair are not already in the list, add them
    if not (i,x) in words_counted:
        words_counted.append((i,x))
    # print one status message for each 500 words processed
    if not len(words_counted) % 500 and statuscounter != len(words_counted):
            print(len(words_counted), "words processed.")
            statuscounter = len(words_counted)

print("Total words processed:", len(words_counted))

# sort the word-and-count list by word
words_counted = sorted(words_counted, key=lambda word: word[0])

# Remove any existing copy of the output CSV file
if os.path.isfile("eventwordscount.csv"):
    os.remove("eventwordscount.csv")

# write this to csv file
with open('eventwordscount.csv', 'w') as fp:
    wr = csv.writer(fp, delimiter=',')
    wr.writerow(('Word','Count'))
    for line in words_counted:
        wr.writerow(line)
fp.close()
print("\nTwo csv files written.")
