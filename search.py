import pandas as pd
import numpy as np
import datetime as dt
from dateutil.parser import parse


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


    
    
    
    
    
    
    
    
    
    
    
    
    
    
