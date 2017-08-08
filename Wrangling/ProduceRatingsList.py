# coding: utf-8
# Use algorithem to choose final event ratings from team members' aggregate scores
# Melanie Huston
# August 2017

# DONE: Read in aggregate ratings csv file and
# DONE: Read in original event list with metadata for each event
# DONE: Choose final numeric rating for each event number according to algorithm
# DONE: Merge final ratings and event metadata
# DONE: Write final event ratings and metadata to csv file

import pandas as pd
import os
import csv

# Initialize our data grids and csv filenames
columns1 = ['EventID', 'Date', 'EventText', 'FilterWords', 'FinalRating']
df_output = pd.DataFrame(index=None, columns=columns1)
dict_ratings = {}

csv_aggregateinput = 'Events_Agg_Results.csv'
csv_eventmetadata = 'Events_SecondLevel.csv'
csv_allratings = 'Events_FinalRatingsList.csv'

# Remove any existing copy of the output CSV file
if os.path.isfile(csv_allratings):
    os.remove(csv_allratings)

# Use algorithm to choose the final rating for each event (mode or average) and write to dictionary
# Use mode if it exists and is between 0 and 3
# Else use average if it is between 0 and 3
# Else assign -1 as the final rating
with open(csv_aggregateinput, 'r') as aggfile:
    print('Processing aggregate ratings\n')
    readthing = csv.DictReader(aggfile)
    headers1 = readthing.fieldnames
    for row in readthing:
        if not row['EventID'] is None:
            if -1.0 < float(row['Mode']) < 4.0:
                finalrating = row['Mode']
            elif -1.0 < float(row['Average']) < 4.0:
                finalrating = float(row['Average'])
            else:
                finalrating = -1.0
            dict_ratings.update({row['EventID'] : finalrating})
aggfile.close()

print('Number of ratings is', len(dict_ratings))

# Read in event metadata and combine with final event rating
with open(csv_eventmetadata, 'r') as finalfile:
    print('\nProcessing event metadata\n')
    readthing = csv.DictReader(finalfile)
    headers2 = readthing.fieldnames
    for row in readthing:
        df_output = df_output.append({'EventID': row['EventID'],
                                      'Date': row['Date'],
                                      'EventText': row['EventText'],
                                      'FilterWords': row['FilterWords'],
                                      'FinalRating': dict_ratings[row['EventID']]},
                                      ignore_index=True)
finalfile.close()

print(df_output)

# Write all events and final ratings to a csv
with open(csv_allratings, 'w') as f_all:
    df_output.to_csv(f_all, header=True, index=False)
f_all.close()

print('One csv file written')
