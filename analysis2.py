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


#%% Most used Apps


# q26 = [q.lower() for q in data["Q26"]]

# twenty_six = pd.DataFrame(data['Q26'])

# twenty_six['Q26'][17] = 'Taobao'
# twenty_six['Q26'][51] = 'Twitter'
# twenty_six['Q26'][41] = 'TikTok'
# twenty_six['Q26'][39] = 'Messages'

# twenty_six['Q26'] = [q.replace("Youtube", "YouTube").replace("iMessages", "Messages").replace("Tiktok", "TikTok").replace("imessage", "Messages").replace("Red book", "Xiaohongshu").replace("Little Red Book", "Xiaohongshu").replace("instagram", "Instagram").strip() for q in twenty_six['Q26']]

# valCountApps = pd.DataFrame(
#     {"App": twenty_six['Q26'].value_counts().index, 
#      "Count": twenty_six['Q26'].value_counts()
#      }).reset_index(drop=True)

# valCountsLots = valCountApps[valCountApps["Count"]> 1]
# valCountsNotLots = valCountApps[valCountApps["Count"] == 1]
# plt.barh(valCountsLots.App, valCountsLots.Count, color = "darkred")
# plt.title("Most Used Apps Frequency")
# plt.xlabel("Apps")
# plt.ylabel("Frequency")

# print(valCountsNotLots)

#%%





#%% ESTIMATED & ACTUAL(Q24) HOURS

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


actualHrs = convert_to_numerical_time(data['Q24'])


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

hrDiff = [estimatedHrs[h] - actualHrs[h] for h in list(range(0, len(estimatedHrs)))]

hrDiff = [float(hr) for hr in hrDiff]
actualHrs = [float(hr) for hr in actualHrs]
estimatedHrs = [float(hr) for hr in estimatedHrs]

#  RESET INDEX
data.reset_index(drop = True, inplace= True)

#%% 

#%% Q2: NUM OF SMARTPHONE DEVICES

def convertSmartphoneDevices(strNum):
    if(strNum == '2' or strNum == '1'): 
        return int(strNum)
    else:
        # print(strNum)
        return 3
        
smartphoneDevices = [convertSmartphoneDevices(i) for i in data['Q2']]


#%% 

# FUNCTION FOR YES:1 AND NO:0
def convertYesNo(resp):
    if(resp == 'No'):
        return 0
    else:
        return 1
#FUNCTION TO CONVERT BINARY VAR USING THE RESPONSE AND A TERM TO MAKE IT 1
def convertBinary(resp, term):
    if(resp == term): return 1
    else: return 0



#%% Q11 TYPES OF SCREEN REDUCTION TECHNIQUES

def convertRedTechToList(s):
    s = s.replace("family, friends,","family friends").replace("computer, keep", "computer keep").replace("brightness, set", "brightness set").replace("silent, face-down, out of sight,", "silent face-down out of sight ").replace(" white), and chan", " white) and chan")
    return s.split(",")

redTechniques = [convertRedTechToList(s) for s in data['Q11']]
redTechniquesAmt = [len(s) for s in redTechniques]

#%%

#%% Q48: AGE OF FIRST SMARTPHONE

def rangeAvg(strRange):
    if(strRange=="18+"): return 18
    strList= strRange.split("-")
    intRange = [int(s) for s in strList]
    return sum(intRange)/2
    
firstSmartphoneAge = [rangeAvg(r) for r in data['Q48']]

#%%



#%% ONE LINER CONVERSIONS

# Q9: USES SCREEN REDUCTION TECHNIQUES (1 if use them, 0 if not)
usesScreenRedTech = [convertYesNo(r) for r in data['Q9']]

# Q39: GENDER
genderDummy = [0 if g=="Male" else 1 for g in data['Q39'] ]

# Q42: Amt of Classes

classesAmt = [7 if a=="7+" else int(a) for a in data['Q42'] ]

# Q44: Amt of Clubs
clubsAmt = [5 if a=="5+" else int(a) for a in data['Q44'] ]

# Q43: Greek Life (1 if involved, 0 if not invovled)
greekLife = [convertYesNo(r) for r in data['Q43']]

#%%

#%%  DUMMY VARIABLES
# Q25:ACTUAL HIGHEST CATEGORY 
highestActSocial = [convertBinary(s, "Social") for s in data['Q25'] ]
highestActUtilities = [convertBinary(s, "Utilities") for s in data['Q25'] ]
highestActProdFin = [convertBinary(s, "Productivity and Finance") for s in data['Q25'] ]

correctlyAssumeCategory = [1 if e==data['Q25'][i] else 0 for i,e in enumerate(data['Q7'])]

#%%


#%% DUMMY VARIABLES LIST: Q3, Q4


def commonActivites(a):
    a = a.replace("calendar, notes, school", "calendar notes school")
    return(a.split(","))

commonActivitiesReported = [commonActivites(a) for a in data['Q3'] ]
commonActivitiesReportedAmt = [len(a) for a in commonActivitiesReported]

#%%




#%% ALL DATA FOR REGRESSION & PLOTS

organizedData = pd.DataFrame(data = {"hrDiff": hrDiff,
                                     "age": data['Q38'], 
                                     "gender": genderDummy,
                                     "classesAmt": classesAmt, 
                                     "clubsAmt": clubsAmt,
                                     "greekLife": greekLife,
                                     "firstSmartphoneAge": firstSmartphoneAge,
                                     "highestActualSocial": highestActSocial,
                                     "highestActualUtilities": highestActUtilities,
                                     "highestActualUProdNFin": highestActProdFin,
                                     "correctlyAssumeCategory": correctlyAssumeCategory,
                                     "commonActivitesReportedAmt": commonActivitiesReportedAmt,
                                     "smartphoneDevices" : smartphoneDevices,
                                     "usesScreenRedTech": usesScreenRedTech,
                                     "RedTechnAmt": redTechniquesAmt,
                                     "actualHrs": actualHrs, 
                                     "estimatedHrs": estimatedHrs
                                      })

#%% 

#%% ANOVA

from scipy.stats import f_oneway

#%%


#%% PLOTTING ESTIMATE ERROR


organizedData = organizedData.drop(12)
organizedData.reset_index(drop=True)

posPred = organizedData[organizedData["hrDiff"] > 0]
negPred = organizedData[organizedData["hrDiff"] <= 0]



plt.scatter(negPred["age"], negPred["hrDiff"], color = 'darkred')
plt.scatter(posPred["age"], posPred["hrDiff"], color = 'darkgreen')

plt.axhline(y = 0.5, color = 'black', linestyle = '-') 
plt.xlabel("Age")
plt.ylabel("Average Daily Screen Time Error")
plt.title("Actual - Estimated Daily Screen Time by Age")









#%%



