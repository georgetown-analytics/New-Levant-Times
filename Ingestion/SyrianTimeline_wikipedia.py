# coding: utf-8
# BeautifulSoup4 event parser for Wikipedia Syrian Civil War timeline pages
# Melanie Huston
# July 2017

# UNDO: Remove footnote references from each event description
# DONE: scrape year from the HTML instead of hard-coding
# DONE: Handle annotations in date headings
# DONE: Handle event descriptions in both p and li tags
# DONE: Iterate through all timeline pages and scrape them
# DONE: Write these data to one CSV file of all events
# TO DO: Store footnote reference domain(s) for each event description
# TO DO: Separately store the date spans and events that do not match the single day format, for human review
# DONE?: Error handling and status messages


import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Wikipedia page containing links to all timeline pages
Timeline_index_URL = 'https://en.wikipedia.org/wiki/Timeline_of_the_Syrian_Civil_War'

csvname = 'Syriantimelinefinal.csv'

## Function scrapepage that does all of the processing of each timeline page - Begin

def scrapepage(URLtoscrape, pagetype, csv_output_filename):

    # Get year from the URL
    URLyear = re.search('\d{4}', URLtoscrape)
    EventYear = URLyear.group(0)

    # Get and parse HTML from the URL
    page = requests.get(URLtoscrape)
    soup = BeautifulSoup(page.content, 'html.parser')

    ## Collect messages from Wikipedia regarding questionable information - Begin
    issuetext = ""

    # issues with the article are displayed in these tables
    issuecheck = soup.find('table', class_='ambox')

    while issuecheck:
        # if issue table is found, discard collapsed text
        for hiddenspan in issuecheck.find_all("span", {'class': 'hide-when-compact'}):
            hiddenspan.decompose()
        # find issue statements in these spans and tighten up the text
        for row in issuecheck.find_all('span', class_='mbox-text-span'):
            if row.text:
                issuemessage = re.sub("\(Learn how.*", "", row.text)
                issuemessage = re.sub("Please.*\.", "", issuemessage)
                issuetext = issuetext + issuemessage
        issuecheck = soup.find_next('table', class_='ambox')

    if issuetext:
        print(soup.title.string, ":", issuetext)
    ## Collect messages from Wikipedia regarding questionable information - End

    # Initialize lists of event dates, annotations and descriptions
    datelist = []
    annotationlist = []
    eventlist = []

    ## Handle standard page or other format - Begin
    if pagetype == 'standard': # handles most pages

        # Find all of the spans with this class, because they contain the event dates. These spans are within h3 tags.
        datething = soup.find_all('span', class_='mw-headline')

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

    else: # process the page with non-conforming formatting

        # Find all of the h3s, because they precede the events
        datething = soup.find_all('h3')

        # For each h3 on the page
        for item in datething:

            # if the h3 contains a span with this class, start looking for the next li (list item) tag
            if item.find('span', class_='mw-headline'):
                findnextli = item.find_next()

                # while there are li tags and they are not the next h3 and not the References section
                # store the date from within the b tags
                while findnextli.name != "h3" and findnextli.text != "References":
                    if findnextli.name == "li":
                        newdatetext = findnextli.b.string
                        if newdatetext and re.match(".*\d+.*", newdatetext):
                            datetext = newdatetext

                        # if there is not a nested list (ul) within this list item, process it as an event and store the date
                        if not findnextli.find('ul'):
                            if datetext:
                                datelist.append(datetext)

                            # get the event text. Remove the date, extra characters and footnote numbers
                            event = findnextli.text
                            if event:
                                eventtext = re.sub("^" + newdatetext, "", event)
                                eventtext = re.sub("^\W\s", "", eventtext)  # "^(\W*\s+)?"
                                eventtext = re.sub("\[\d+\]", "", eventtext)
                                eventlist.append(eventtext)

                                # insert blank annotation entry
                                annotationlist.append('')

                    findnextli = findnextli.find_next()
    ## Handle standard page or other format - End

    # If events were found for this page, put the date, year, event description and other data into a dataframe
    if len(eventlist):
        datatable = pd.DataFrame(datelist, columns=['Date'])
        datatable['Year'] = EventYear
        datatable['Annotation'] = annotationlist
        datatable['Event'] = eventlist
        datatable['Issue(s)'] = issuetext
        datatable['Source'] = soup.title.string
        datatable['Source URL'] = URLtoscrape

        # Print status message
        print("Number of events for", datelist[0], "to", datelist[-1], EventYear, "=", len(eventlist))

        # Write if csv file doesn't exist , or append if csv file exists already
        if not os.path.isfile(csv_output_filename):
            with open(csv_output_filename, 'w') as f_new:
                datatable.to_csv(f_new, header=True, index=False)
                f_new.close()
        else:
            with open(csv_output_filename, 'a') as f_append:
                datatable.to_csv(f_append, header=False, index=False)
                f_append.close()
    else:
        # no events were found on this page
        print("Number of events for", soup.title.string, "= 0")

    # return the number of events found for this page
    return len(eventlist)

## Function scrapepage that does all of the processing of each timeline page - End


## START HERE

# Remove any existing copy of the output CSV file
if os.path.isfile(csvname):
    os.remove(csvname)

# Get the content of the Wikipedia page containing links to all timeline pages
page = requests.get(Timeline_index_URL)
indexsoup = BeautifulSoup(page.content, 'html.parser')

# Initialize for the total number of events collected and pages scraped
TotalEvents = 0
PagesProcessed = 0

# Find all of the a tags containing "Timeline of the Syrian Civil War..."
# as link text so we can scrape each one for events
indexthing = indexsoup.find_all('a')

for item in indexthing:
    if re.match("Timeline of the Syrian Civil War.*\)",item.text):
        URLmeat = item.get('href')
        theURL = "https://en.wikipedia.org" + URLmeat
        if not (re.search("January–April 2011", item.text)):
            URLEvents = scrapepage(theURL,"standard", csvname)
        else: # process January-April 2011 as non-standard event format
            URLEvents = scrapepage(theURL, "non-standard", csvname)
        TotalEvents = TotalEvents + URLEvents
        PagesProcessed +=1

print("Total events collected =", TotalEvents, "from", PagesProcessed, "pages")

## END HERE
