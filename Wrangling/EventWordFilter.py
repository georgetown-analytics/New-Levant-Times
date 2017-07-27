# coding: utf-8
# Two-level term filter for "Event" description field in csv file output
# from SyrianTimeline_wikipedia.py: Syriantimelinefinal.csv
# Melanie Huston
# July 2017

# DONE: Scrape web page of diplomatic vocabulary terms and prepare for first-level filtering
# DONE: Filter syrian events from csv of all events for first level
# DONE: Filter output of first-level filter through second-level filter.
# DONE: Write output of both filter levels to CSV files
# TO DO: Generate unique event IDs in the prior step with SyrianTimeline_wikipedia.py
# TO DO: create parsible dates using the Date and Year fields prior to this step
# DONE?: Error handling and status messages
# Note: Second-level filter terms selected by manual review of output from EventWordCount.py


import re
import pandas as pd
import os
import csv
import requests
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

rowcount = 0
firstrelevantevents = 0
secondrelevantevents = 0
firstfilterwords = []
csv_eventsalllevels = 'Events_AllLevels.csv'
csv_eventssecondlevel = 'Events_SecondLevel.csv'
i = 0

# Remove any existing copies of the output CSV files
if os.path.isfile(csv_eventsalllevels):
    os.remove(csv_eventsalllevels)
if os.path.isfile(csv_eventssecondlevel):
    os.remove(csv_eventssecondlevel)

# Initialize our dataframe of events
columns = ['EventNo', 'Date', 'Year', 'EventText', 'FilterWords', 'Level']
ourdiploevents = pd.DataFrame(index=None, columns=columns)

# First Filter Terms
# Web page "250 words from the domain of diplomacy" September 8, 2012
diplovocabURL = 'https://www.vocabulary.com/lists/183677'

# Get and parse HTML
page = requests.get(diplovocabURL)
soup = BeautifulSoup(page.content, 'html.parser')

# Find and stem all linked vocabulary terms for the first filter
diplowords = soup.find_all('a', class_='dynamictext')
for dip in diplowords:
    # apply Porter stemmer to term
    stemdip = stemmer.stem(dip.text)
    # remove final 'i' from stemmed term to accommodate singular and plural variants. E.g., 'embassi'
    stemdip = re.sub('i$', '', stemdip)
    # ensure diplomatic filter terms are in lower case
    stemdip = str.lower(stemdip)
    firstfilterwords.append(stemdip)

# Second Filter Terms
# Add human-selected lower-case terms for a second filter. please maintain in alpha order.
secondfilterwords = ['america', 'brit', 'china', 'egypt', 'e.u', 'emirat', 'franc',
                     'fren', 'iran', 'iraq', 'israel', 'jordan', 'kurd',
                     'league', 'libya', 'leban', 'nation', 'oman', 'qatar',
                     'russ', 'saudi', 'sudan', 'turk', 'u.a.e', 'u.s', 'u.k', 'united']

# First Filter - BEGIN
# read each event from the csv file output from SyrianTimeline_wikipedia.py
with open('Syriantimelinefinal.csv', 'r') as csvfile:
    readthing = csv.reader(csvfile)
    next(readthing) # skip header row
    for row in readthing:
        rowcount += 1
        eventwords = str.lower(row[3]) # look at the lower-case event description
        for target in firstfilterwords:
            # when a word from the first-level filter list is found,
            # write a row to the dataframe and move on to the next event desc
            if target in eventwords:
                firstrelevantevents += 1
                ourdiploevents = ourdiploevents.append({'EventNo': firstrelevantevents,
                                                        'Date': row[0],
                                                        'Year': row[1],
                                                        'EventText': row[3],
                                                        'FilterWords': target,
                                                        'Level': 'first'},
                                                       ignore_index=True)
                break
        # print status message for each 100 events processed
        if not rowcount % 100:
            print(rowcount, "events processed.\n")
csvfile.close()
print(firstrelevantevents, "total events caught by first filter.\n")

# Convert the event number from a float to an integer
ourdiploevents['EventNo'] = ourdiploevents['EventNo'].astype(int)
# First Filter - END

# Second Filter - BEGIN
# Filter events caught by the first-level filter through the second-level filter
while i < firstrelevantevents:
    event = ourdiploevents.loc[i, 'EventText']
    # Check for these acronyms and words with caps
    if 'EU' in event or 'UAE' in event or 'UK' in event or 'US' in event or 'Union' in event:
        secondrelevantevents += 1
        ourdiploevents.loc[i, 'FilterWords'] = ourdiploevents.loc[i, 'FilterWords'] + ', capitalletters'
        ourdiploevents.loc[i, 'Level'] = 'second'
    # Otherwise, check for our second level filter words in lower case
    else:
        for target in secondfilterwords:
            if target in str.lower(event):
                secondrelevantevents += 1
                ourdiploevents.loc[i, 'FilterWords'] = ourdiploevents.loc[i, 'FilterWords'] + ', ' + target
                ourdiploevents.loc[i, 'Level'] = 'second'
                break
    i += 1

print(secondrelevantevents, "total events output by second filter.\n")
# Second Filter - END

# Write all events caught by all filters to a csv
with open(csv_eventsalllevels, 'w') as f_all:
    ourdiploevents.to_csv(f_all, header=True, index=False)
    f_all.close()

# Write only the events caught by the second filter to a csv
seconddiploevents = ourdiploevents[ourdiploevents['Level'] == 'second']

with open(csv_eventssecondlevel, 'w') as f_second:
    seconddiploevents.to_csv(f_second, header=True, index=False)
    f_second.close()

print("Two csv files written.")


