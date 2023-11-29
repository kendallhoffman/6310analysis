#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 21:45:28 2023

@author: medhabulumulla

Code file to clean the data retreived from Qualtrics for INFO 6310
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



