# coding: utf-8
# Assign three reviewers to each event filtered by EventWordFilter.py
# using output Events_SecondLevel.csv
# Melanie Huston
# July 2017

import re
import pandas as pd
import os
import csv
import requests

personlist = ["Carl", "Gerhard", "Makida", "Melanie", "Michael"]

# Generated all possible 5 choose 3 combinations = 10 subsets
peoplelists = [
"Melanie | Michael | Makida", 
"Carl | Michael | Makida",
"Carl | Melanie | Makida",
"Carl | Melanie | Michael",
"Gerhard | Michael | Makida",
"Gerhard | Melanie | Makida",
"Gerhard | Melanie | Michael",
"Gerhard | Carl | Makida",
"Gerhard | Carl | Michael",
"Gerhard | Carl | Melanie"    
]

reset = len(peoplelists)

# Initialize our dataframes of assignments
columns1 = ['EventNo', 'Date', 'Year', 'EventText', 'People']
df_all = pd.DataFrame(index=None, columns=columns1)
columns2 = ['EventNo', 'Date', 'Year', 'EventText', 'Person']
df_person = pd.DataFrame(index=None, columns=columns2)

csv_allassignments = 'Events_AllAssignments.csv'
csv_assignmentbyperson = 'Events_AssignedbyPerson.csv'
assignmentrow = 0

# Remove any existing copies of the output CSV files
if os.path.isfile(csv_allassignments):
    os.remove(csv_allassignments)
if os.path.isfile(csv_assignmentbyperson):
    os.remove(csv_assignmentbyperson)

# Assign a three-person combination to each event - Begin
with open('Events_SecondLevel.csv', 'r') as csvfile:
    readthing = csv.reader(csvfile)
    next(readthing) # skip header row
    for row in readthing:
        # calculate the index of the next combination from peoplelists
        index = assignmentrow % reset

        df_all = df_all.append({'EventNo': row[0],
                                'Date': row[1],
                                'Year': row[2],
                                'EventText': row[3],
                                'People': peoplelists[index]},
                                ignore_index=True)
        assignmentrow += 1
        # print status message for each 100 events assigned
        if not assignmentrow % 100:
            print(assignmentrow, "events assigned.\n")
csvfile.close()
print(assignmentrow, "total events assigned.\n")
# Assign a three-person combination to each event - End

# Create a list of all events assigned to each individual person - Begin
for i, assignment in df_all.iterrows():
    for person in personlist:
        if person in assignment['People']:
            df_person = df_person.append({'EventNo': assignment['EventNo'],
                                          'Date': assignment['Date'],
                                          'Year': assignment['Year'],
                                          'EventText': assignment['EventText'],
                                          'Person': person},
                                          ignore_index=True)

# Create a list of all events assigned to each individual person - End

# Display the review burden for each team member
print(df_person['Person'].value_counts())

# Write the three assigned people per event to a csv
with open(csv_allassignments, 'w') as f_all:
    df_all.to_csv(f_all, header=True, index=False)
    f_all.close()

# Sort the assigned individual list by name
df_person = df_person.sort_values('Person')

# Write the events assigned to each individual to a csv
with open(csv_assignmentbyperson, 'w') as f_second:
    df_person.to_csv(f_second, header=True, index=False)
    f_second.close()

print("Two csv files written.")


