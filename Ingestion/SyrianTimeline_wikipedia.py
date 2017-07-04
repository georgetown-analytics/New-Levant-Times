# coding: utf-8
# BeautifulSoup4 event parser for Wikipedia Syrian Civil War timeline pages
# Melanie Huston
# July 2017

# TO DO: Remove footnote references from each event description
# TO DO: scrape year from the HTML instead of hard-coding
# TO DO: Iterate through all timeline pages and scrape them
# TO DO: Write these data to one CSV file of all events
# TO DO: Separately store the date spans and events that do not match the single day format, for human review
# TO DO: Error handling


import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Scrape data from one timeline page.
URLtoscrape = 'https://en.wikipedia.org/wiki/Timeline_of_the_Syrian_Civil_War_(January–April_2016)'


# Hard-code year for now.
EventYear = "2016"

# Get and parse HTML from the URL
page = requests.get(URLtoscrape)
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify()) -- uncomment to see the HTML source

# Find all of the spans with this class, because they contain the event dates. These spans are within h3 tags.
datething = soup.find_all('span', class_='mw-headline')

# Initialize lists of event dates and event descriptions
datelist = []
eventlist = []

# For each event date span on the page
for item in datething:


    # Get the text from within the span
    datetext = item.find(text=True)

    # If the text looks like a number and a month (a specific day), store the date and the event(s)
    if re.match("\d+ [a-zA-Z]+", datetext):

        # For this day, find and store the event description(s) from the next paragraph tag(s)
        nextthing = item.findNext('p')

        # while there are p tags and they are not the next day (next h3)
        # and not in the References section, store the date with each event description
        while nextthing.name != "h3" and nextthing.text != "References":
            if nextthing.name == "p":
                datelist.append(datetext)
                eventtext = nextthing.text
                eventlist.append(eventtext)
            nextthing = nextthing.find_next()


# Put the date, year, and event description into a dataframe
datatable = pd.DataFrame(datelist,columns=['Date'])
datatable['Year'] = EventYear
datatable['Event'] = eventlist

# Print the dataframe to prove this works
print(datatable)

