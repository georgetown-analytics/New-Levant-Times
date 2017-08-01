# coding: utf-8
# Compile and average event ratings from all team members' review spreadsheets
# Melanie Huston
# July 2017

# DONE: Read in each team member's csv file and extract numeric ratings
# DONE: Generate mean score for each event
# TO DO: remove "_Test" text from glob statement
# TO DO: Write aggregate event scores to csv file

import re
import pandas as pd
import os
import glob
import csv
import requests
import numpy as np

# Initialize our dataframe of ratings
columns1 = ['EventID', 'Date', 'EventText', 'Rating', 'Person']
df_ratings = pd.DataFrame(index=None, columns=columns1)

csv_allratings = 'Events_AllRatings.csv'

# Remove any existing copy of the output CSV file
if os.path.isfile(csv_allratings):
    os.remove(csv_allassignments)

for file in glob.glob('Events_Assigned_Test*.csv'):
    with open(file, 'r') as personfile:
        readthing = csv.reader(personfile)
        next(readthing)
        for row in readthing:
            if row[0]:
                ratingfield = re.search('\d+', row[4])
                if ratingfield:
                    ratingnumber = ratingfield.group(0)
                else:
                    ratingnumber = float('nan')
                df_ratings = df_ratings.append({'EventID': row[0],
                                        'Date': row[1],
                                        'EventText': row[3],
                                        'Rating': ratingnumber,
                                        'Person': row[5]},
                                       ignore_index=True)
    personfile.close()

df_ratings['EventID'] = df_ratings['EventID'].astype(int)
df_ratings['Rating'] = df_ratings['Rating'].astype(float)

print(df_ratings.describe())

# df_eventgroups = df_ratings.groupby('EventID')
# df_avgratings = df_eventgroups['Rating'].agg([np.mean]).rename(columns={'mean': 'AvgRating'})

df_ratings['AvgRating'] = df_ratings.groupby('EventID')['Rating'].transform(np.mean)
print("\nAvg ratings head")
print(df_ratings)

