# coding: utf-8
# Compile and average event ratings from all team members' review spreadsheets
# Melanie Huston
# July 2017

# DONE: Read in each team member's csv file and extract numeric ratings
# DONE: Generate mean score for each event
# DONE: remove "_Test" text from glob statement
# TO DO: Get data by column heading instead of index
# TO DO: Write aggregate event scores to csv file

import re
import pandas as pd
import os
import glob
import csv
import requests
import numpy as np
from itertools import *

# Initialize our dataframe of ratings
columns1 = ['EventID', 'Date', 'EventText', 'Rating', 'Person']
df_ratings = pd.DataFrame(index=None, columns=columns1)
badevents = pd.DataFrame(index=None, columns=columns1)
columns2 = ['EventID','Date', 'EventText', 'AvgRating', 'Agreement']
df_output = pd.DataFrame(index=None, columns=columns2)
csv_allratings = 'Events_AllRatings.csv'

# Remove any existing copy of the output CSV file
if os.path.isfile(csv_allratings):
    os.remove(csv_allassignments)

for file in glob.glob('Events_Assigned_*.csv'):
    with open(file, 'r') as personfile:
        print('Processing', file)
        readthing = csv.DictReader(personfile)
        headers = readthing.fieldnames
        for row in readthing:
            if row['EventID']: # if there is an event ID in this row
                ratingfield = re.search('\d+', row['Rating'])
                if not ratingfield is None:
                    ratingnumber = ratingfield.group(0) # pull the number out of the rating field
                    df_ratings = df_ratings.append({'EventID': row['EventID'],
                                                    'Date': row['Date'],
                                                    'EventText': row['EventText'],
                                                    'Rating': ratingnumber,
                                                    'Person': row['Person']},
                                                   ignore_index=True)
                else:
                    ratingnumber = float('nan') # or set the rating to not a number
                    badevents = badevents.append({'EventID': row['EventID'],
                                        'Date': row['Date'],
                                        'EventText': row['EventText'],
                                        'Rating': row['Rating'],
                                        'Person': row['Person']},
                                       ignore_index=True)
    personfile.close()

df_ratings['EventID'] = df_ratings['EventID'].astype(int)
df_ratings['Rating'] = df_ratings['Rating'].astype(float)

# df_eventgroups = df_ratings.groupby('EventID')
# df_avgratings = df_eventgroups['Rating'].agg([np.mean]).rename(columns={'mean': 'AvgRating'})
df_ratings['AvgRating'] = df_ratings.groupby('EventID')['Rating'].transform(np.mean)
#for index, row in df_ratings:
#    row[index,'Agreement'] = row[index,'AvgRating'].is_integer()

print('i got this far woo hooooo\n')
for index, row in islice(df_ratings.iterrows(), 1, None):
    print(index)
    print(row.loc[index,'EventID'])
    if row.loc[index,'EventID'] not in df_output.frame['EventID']:
        df_output = df_output.append({'EventID': row.loc[index,'EventID'],
                                                        'Date': row.loc[index,'Date'],
                                                        'EventText': row.loc[index,'EventText'],
                                                        'AvgRating': row.loc[index,'AvgRating'],
                                                        'Agreement': row.loc[index,'AvgRating'].is_integer()},
                                                       ignore_index=True)
print(df_output)

print(df_ratings)

print("\nBad Events")
print(badevents)

# >>> (1.0).is_integer()
# True
# >>> (1.555).is_integer()
# False