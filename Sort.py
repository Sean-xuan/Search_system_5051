# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 14:14:07 2022

@author: brynn
"""

import pandas as pd
import numpy as np
import datetime as dt
from dateutil.parser import parse
#%% search
'''   
 0   VehicleType      259623 non-null  int64  
 1   DerectionTime_O  259623 non-null  object 
 2   GantrylD_O       259623 non-null  object 
 3   DerectionTime_D  259623 non-null  object 
 4   GantrylD_D       259623 non-null  object 
 5   TripLength       259623 non-null  float64
 6   TripEnd          259623 non-null  object 
 7   TripInformation  259623 non-null  object     
'''

filepath = r"D:\code\date.csv"

class Traffic_inquiry():
    def __init__(self,filepath):
        self.filepath = filepath
        self.df = pd.read_csv(self.filepath,header = None)
        self.df.columns = ['VehicleType','DerectionTime_O','GantrylD_O',
              'DerectionTime_D','GantrylD_D','TripLength',
              'TripEnd','TripInformation']
        
        
    def search(self,columns,keywords):
    # no keywords
        if keywords==['','']:
            return self.df
        # only 1 keyword
        elif '' in keywords:
            if keywords[0]=='':
                column,keyword = columns[1],keywords[1]
            else:
                column,keyword = columns[0],keywords[0]
            # fuzzy match
            if column in ['DerectionTime_O','DerectionTime_D','TripInformation']:
                return self.df[self.df[column].astype(str).str.contains(keyword)].reset_index(drop=True)
            else:
                # exact match
                return self.df[self.df[column].isin([keyword])].reset_index(drop=True)
        # 2 keywords    
        else:
            if columns[0]==columns[1]:
                # return an arange
                if columns[0] in ['DerectionTime_O','DerectionTime_D','TripLength']:
                    if columns[0]=='TripLength':
                        return self.df[self.df[columns[0]].between(float(min(keywords)),float(max(keywords)))].reset_index(drop=True)
                    # str to datetime to str
                    keywords = [str(pd.to_datetime(keywords)[i]) for i in [0,1]]
                    return self.df[self.df[columns[0]].between(min(keywords),max(keywords))].reset_index(drop=True)
                
                elif columns[0] in ['VehicleType','GantrylD_O','GantrylD_D','TripEnd']:
                     # exact match
                    return self.df[self.df[columns[0]].isin(keywords)].reset_index(drop=True)
                else:
                    # fuzzy match 
                    return self.df[(self.df[columns[0]].astype(str).str.contains(keywords[0]))
                              &(self.df[columns[1]].astype(str).str.contains(keywords[1]))].reset_index(drop=True)
            else:
                length = len(set(columns)&(set(['DerectionTime_O','DerectionTime_D','TripInformation'])))
                if length==2:
                    # fuzzy match
                    return self.df[(self.df[columns[0]].astype(str).str.contains(keywords[0]))
                              &(self.df[columns[1]].astype(str).str.contains(keywords[1]))].reset_index(drop=True)
                elif length==1:
                    # fuzzy match with exact match
                    if columns[0] in ['DerectionTime_O','DerectionTime_D','TripInformation']:
                        return self.df[(self.df[columns[0]].astype(str).str.contains(keywords[0]))
                                  &(self.df[columns[1]].isin([keywords[1]]))].reset_index(drop=True)
                    else:
                        return self.df[(self.df[columns[1]].astype(str).str.contains(keywords[1]))
                                  &(self.df[columns[0]].isin([keywords[0]]))].reset_index(drop=True)
                else:
                    # exact match
                    return self.df[(self.df[columns[0]].isin([keywords[0]]))&(self.df[columns[1]].isin([keywords[1]]))].reset_index(drop=True)


# test for class
a = Traffic_inquiry(filepath)
b = a.search(['GantrylD_D','TripEnd'],['03F1991S','Y'])        


def search2(df,columns,keywords):
    # no keywords
    if keywords==['','']:
        return df
    # only 1 keyword
    elif '' in keywords:
        if keywords[0]=='':
            column,keyword = columns[1],keywords[1]
        else:
            column,keyword = columns[0],keywords[0]
        # fuzzy match
        if column in ['DerectionTime_O','DerectionTime_D','TripInformation']:
            return df[df[column].astype(str).str.contains(keyword)].reset_index(drop=True)
        else:
            # exact match
            return df[df[column].isin([keyword])].reset_index(drop=True)
    # 2 keywords    
    else:
        if columns[0]==columns[1]:
            # return an arange
            if columns[0] in ['DerectionTime_O','DerectionTime_D','TripLength']:
                if columns[0]=='TripLength':
                    return df[df[columns[0]].between(float(min(keywords)),float(max(keywords)))].reset_index(drop=True)
                # str to datetime to str
                keywords = [str(pd.to_datetime(keywords)[i]) for i in [0,1]]
                return df[df[columns[0]].between(min(keywords),max(keywords))].reset_index(drop=True)
            
            elif columns[0] in ['VehicleType','GantrylD_O','GantrylD_D','TripEnd']:
                 # exact match
                return df[df[columns[0]].isin(keywords)].reset_index(drop=True)
            else:
                # fuzzy match 
                return df[(df[columns[0]].astype(str).str.contains(keywords[0]))
                          &(df[columns[1]].astype(str).str.contains(keywords[1]))].reset_index(drop=True)
        else:
            length = len(set(columns)&(set(['DerectionTime_O','DerectionTime_D','TripInformation'])))
            if length==2:
                # fuzzy match
                return df[(df[columns[0]].astype(str).str.contains(keywords[0]))
                          &(df[columns[1]].astype(str).str.contains(keywords[1]))].reset_index(drop=True)
            elif length==1:
                # fuzzy match with exact match
                if columns[0] in ['DerectionTime_O','DerectionTime_D','TripInformation']:
                    return df[(df[columns[0]].astype(str).str.contains(keywords[0]))
                              &(df[columns[1]].isin([keywords[1]]))].reset_index(drop=True)
                else:
                    return df[(df[columns[1]].astype(str).str.contains(keywords[1]))
                              &(df[columns[0]].isin([keywords[0]]))].reset_index(drop=True)
            else:
                # exact match
                return df[(df[columns[0]].isin([keywords[0]]))&(df[columns[1]].isin([keywords[1]]))].reset_index(drop=True)
   
# test for function
# df = pd.read_csv(filepath,header = None)
# df.columns = ['VehicleType','DerectionTime_O','GantrylD_O',
#               'DerectionTime_D','GantrylD_D','TripLength',
#               'TripEnd','TripInformation']
# l1 = search2(df,['VehicleType','VehicleType'],['',''])
# l2 = search2(df,['VehicleType','VehicleType'],['31',''])
# l3 = search2(df,['VehicleType','VehicleType'],['','31'])
# l4 = search2(df,['VehicleType','DerectionTime_O'],['','2019-08-30 08:17'])
# l4 = search2(df,['DerectionTime_O','DerectionTime_O'],['2019-08-30 08:16','2019-08-30 08:17'])
# l4 = search2(df,['TripLength','TripLength'],['3','5.2'])
# l4 = search2(df,['TripInformation','TripInformation'],['2019-08-30 08:16','2019-08-30 08:20'])
# l5 = search2(df,['GantrylD_D','DerectionTime_O'],['03F1991S','2019-08-30 08:16'])
# l3 = search2(df,['GantrylD_D','TripEnd'],['03F1991S','Y'])



#%% sort
'''
signal = 0: 升序排序
signal = 1: 降序排序
直接使用 sort(df,columns，signal)函数
'''

df = pd.read_csv('TDCS_M06A_20190830_080000.csv',header = None)
l = len(df)

def quicksort(array):
    if len(set(array)) < 2:
        return array
    pivot = array[0]
    left = [i for i in array[1:] if i <= pivot]
    right = [i for i in array[1:] if i > pivot]
    return quicksort(left)+[pivot]+quicksort(right)

def counting_sort(array):
    max_elem = max(array)
    counts = [0 for i in range(max_elem + 1)]
    for elem in array:
        counts[elem] += 1
    return [i for i in range(len(counts)) for cnt in range(counts[i])] 

def merge_sort(array):
    if len(array) <= 1:
        return array
    mid = (len(array) + 1) // 2
    sub1 = merge_sort(array[: mid])
    sub2 = merge_sort(array[mid :])
    return ordered_merge(sub1, sub2)

def ordered_merge(a1, a2):
    cnt1, cnt2 = 0, 0
    result = []
    while cnt1 < len(a1) and cnt2 < len(a2):
        if a1[cnt1] < a2[cnt2]:
            result.append(a1[cnt1])
            cnt1 += 1
        else:
            result.append(a2[cnt2])
            cnt2 += 1
    result += a1[cnt1 :]
    result += a2[cnt2 :]
    return result

def sort(df,columns,signal):
    df.index = df[columns]
    if columns in [1,2,3,4]:
        a_in = quicksort(df.index)
        a_de = list(reversed(a_in))
    if columns == 0:
        a_in = counting_sort(df.index)
        a_de = list(reversed(a_in))
    if columns == 5:
        a_in = merge_sort(list(df.index))
        a_de = list(reversed(a_in))
         
    
    
    if signal == 0:
        #return df
        return df.reindex(a_in)
    if signal == 1:
        #return df
        return df.reindex(a_de)
    df.index = range(l)
    
##test:
x = sort(df,5,1)
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
