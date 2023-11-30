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
    ansFull = ansFull.replace(",", "").replace("twitter(x)", "twitter").replace("g-mail", "gmail").replace(" x ", " twitter ")
    ansFull = ansFull.replace("neteflix", "netflix").replace("nan", "").replace("monopoly go", "monopoly-go")
    ansFull = ansFull.replace("red book", "red-book ")
    
    ans = ansFull.split(" ")
    qeight.append([app.strip() for app in ans])
    
allqeight = flatten(qeight)

uniqueAllQEight = pd.Series(allqeight).value_counts()

data['Q8'] = qeight
        
        

#%%


#%% Useful Questions

# q1: how many devices do you use
# q6: estimate daily average vs. q24 avg daily screentime
#q7 category vs. q25 most used category



q6 = [d.replace(" hours", "").split("-") for d in data['Q6']]

estimatedHrs = [(int(hrs[1]) + int(hrs[0])) /2 for hrs in q6]


import re

def convert_to_numerical_time(time_list):
    numerical_values = []

    for time_str in time_list:
        # Extract numerical values using regular expressions
        match = re.findall(r'\d+\.\d+|\d+', time_str)
        
        # Convert the extracted values to float and sum them up
        if match:
            total_minutes = sum(float(value) for value in match)
            numerical_values.append(total_minutes)
        else:
            numerical_values.append(None)  # Handle cases where no numerical values are found

    return numerical_values


# Example usage:
actualHrs = convert_to_numerical_time(data['Q24'])

for h,hr in enumerate(actualHrs):
   if(hr is None or float(hr) > 24):
       
       print("IDX:", int(h), "RAW DATA:", data.Q24[int(h)+3], "NEW DATA:", hr)
       

actualHrs[0] = 3 + (38/60)
actualHrs[6] = 2.5
actualHrs[10] = 3 + (40/60)
actualHrs[21] = 7
actualHrs[29] = 5
actualHrs[34] = 5
actualHrs[35] = 10 + (47/60)
actualHrs[36] = 0
actualHrs[41] = 7.3
actualHrs[43] = 3
actualHrs[49] = 7
actualHrs[50] = 3 + (43/60)
actualHrs[54] = 3

import matplotlib.pyplot as plt

hrDiff = [actualHrs[h] - estimatedHrs[h] for h in list(range(0, len(estimatedHrs)))]

hrDiff = [float(hr) for hr in hrDiff]
actualHrs = [float(hr) for hr in actualHrs]
estimatedHrs = [float(hr) for hr in estimatedHrs]


organizedData = pd.DataFrame(data = {"age": data['Q38'], 
                                     "actualHrs": actualHrs, 
                                     "estimatedHrs": estimatedHrs, 
                                     "hrDiff": hrDiff })

organizedData = organizedData.drop(12)
organizedData.reset_index(drop=True)

plt.scatter(organizedData["age"], organizedData["hrDiff"])
plt.scatter(organizedData["age"].astype(int), organizedData["hrDiff"].astype(int))



#%%
