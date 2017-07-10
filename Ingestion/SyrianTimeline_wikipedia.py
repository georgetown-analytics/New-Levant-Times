# coding: utf-8
# BeautifulSoup4 event parser for Wikipedia Syrian Civil War timeline pages
# Melanie Huston
# July 2017

# DONE: Remove footnote references from each event description
# DONE: scrape year from the HTML instead of hard-coding
# DONE: Handle annotations in date headings
# TO DO: Handle event descriptions in both p and li tags
# TO DO: Iterate through all timeline pages and scrape them
# TO DO: Write these data to one CSV file of all events
# TO DO: Separately store the date spans and events that do not match the single day format, for human review
# TO DO: Error handling and status messages


import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Scrape data from one timeline page: test pages
URLtoscrape = 'https://en.wikipedia.org/wiki/Timeline_of_the_Syrian_Civil_War_(January–April_2016)'
#URLtoscrape = 'https://en.wikipedia.org/wiki/Timeline_of_the_Syrian_Civil_War_(September–December_2011)'

# Get year from the URL
URLyear = re.search('\d{4}', URLtoscrape)
EventYear = URLyear.group(0)

# Get and parse HTML from the URL
page = requests.get(URLtoscrape)
soup = BeautifulSoup(page.content, 'html.parser')

# Find all of the spans with this class, because they contain the event dates. These spans are within h3 tags.
datething = soup.find_all('span', class_='mw-headline')

# Initialize lists of event dates, annotations and descriptions
datelist = []
annotationlist = []
eventlist = []

# For each event date span on the page
for item in datething:

    annotationtext = ""

    # Get the text from within the span
    datetext = item.find(text=True)

    # If the text looks like a number and a month (a specific day), store the date and the event(s)
    if re.match("\d+\s[a-zA-Z]+", datetext):

        # If there is an annotation after the day and month, save that to store with the event description(s)
        annotated_date = re.match("(?P<mydate>\d+\s[a-zA-Z]+)\s+(-|--|\\u2013)\s+(?P<annotation>.*)", datetext)
        if annotated_date:
            datetext = annotated_date.group('mydate')
            annotationtext = annotated_date.group('annotation')

        # For this day, find and store the event description(s) from the next paragraph tag(s)
        # nextthing = item.findNext('p')
        nextthing = item.find_next()

        # while there are p tags and they are not the next day (next h3 or h4)
        # and not in the References section, store the date with each event description
        while nextthing.name != "h3" and nextthing.name != "h4" and nextthing.text != "References":
            if nextthing.name == "p" or nextthing.name == "li":
                datelist.append(datetext)
                annotationlist.append(annotationtext)
                eventtext = nextthing.text
                # Remove footnote number(s) in brackets from event description
                eventtext = re.sub("\[\d+\]", "", eventtext)
                eventlist.append(eventtext)

            nextthing = nextthing.find_next()


# Put the date, year, and event description into a dataframe
datatable = pd.DataFrame(datelist,columns=['Date'])
datatable['Year'] = EventYear
datatable['Annotation'] = annotationlist
datatable['Event'] = eventlist
datatable['Source'] = soup.title.string
datatable['Source URL'] = URLtoscrape


# Print the dataframe to prove this works
print(datatable)

with open('Syriantimeline.csv', 'a') as f:
    datatable.to_csv(f, index=False)
    f.close()

