#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 21:45:28 2023

@author: medhabulumulla

Code file to clean the data retreived from Qualtrics for INFO 6310 retreived from Kendall Hoffman
"""

import pandas as pd
import numpy as np


data = pd.read_csv('smartphone_survey_data_11_27_23.csv')

data = data.drop(['StartDate', 'EndDate',  'RecordedDate', 'RecipientLastName', 'RecipientFirstName' , 'RecipientEmail',
                  'ExternalReference', 'LocationLatitude', 'LocationLongitude', 'IPAddress', 
                  'DistributionChannel', 'UserLanguage', 'Duration (in seconds)', 'Q23_Id', 'Q23_Name', 'Q23_Size',
                  'Q23_Type', 'Q30_Id', 'Q30_Name', 'Q30_Size', 'Q30_Type'], axis=1)

#drop rows that aren't 100% progress (aka finished)
data = data[data['Finished'] == 'True']
#drop survey previews
data = data[data['Status'] == 'IP Address']
pd.set_option('display.max_columns', None)


#dealing with the mess that is Q8
# print(data['Q8'])

#split on commas
data['Q8'] = data['Q8'].astype(str) 
data['Q8'] = data['Q8'].str.split(',')

#instances where inputted answer wasn't exactly three apps
diff_data = data[data['Q8'].apply(lambda x: len(x) != 3)]
print(diff_data['Q8'])

#q24 -- input reported screentime from screenshot

data.dropna(subset=['Q24'], inplace=True)
print(data['Q24'])

#Convert 'Q26' column to string
data['Q26'] = data['Q26'].astype(str)

# Convert 'Q8' column to list (if it's not already)
data['Q8'] = data['Q8'].apply(lambda x: [x] if not isinstance(x, list) else x)

# Filter rows where the string in 'Q24' is in the list in 'Q8'
estApps = data[data.apply(lambda row: row['Q26'] in row['Q8'], axis=1)]

# initialize data of lists. 
estApps_data = {'Q26': estApps['Q26'], 
        'Q8': estApps['Q8']} 
  
# Create DataFrame 
df = pd.DataFrame(estApps_data) 
  
# Print the output. 
df

#19 people included their most used app in their estimated most used apps (30%) 
# UNCLEANED THOUGH SO THIS ISNT ACTUALLY TRUE BC PEOPLE MIGHT SPELL THINGS DIFFERENTLY IN DIFFERENT QUESTIONS


# unique counts in q26 (most used app)

data['Q26'].value_counts()

# need to clean this so that different spellings are counted as the same app
#cleaning some of it manually bc that's just easier lmao whoops 


#%% Question 8

# https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
def flatten(l):
    return [item for sublist in l for item in sublist]

# print(data['Q8'])

qeight = []
for ans in data['Q8']:
    ansFull = ''.join(ans).lower()
    ansFull = ansFull.replace("and", " ").replace("tik tok","tiktok").replace("imessages", "imessage").replace(".", "").replace(",", "").replace("instragram", "instagram").replace("what's app", "whatsapp").replace("(social media)", "").replace(",", "").replace(".", "").replace("i think instagram youtube   two dots (a game) are the most used apps", "instagram, youtube")
    ansFull = ansFull.replace("netflitwitter", "netflix, twitter").replace(",", "").replace("twitter(x)", "twitter").replace("x", "twitter").replace("g-mail", "gmail")
    ans = ansFull.split(" ")
    print(ans)
    qeight.append([app.strip() for app in ans])
    
allqeight = flatten(qeight)

uniqueAllQEight = pd.Series(allqeight).value_counts()
        
        

#%%
