
import pandas as pd
import numpy as np
import datetime as dt
from dateutil.parser import parse
import copy


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
    def __init__(self,filepath,searchcolumns,searchkeywords):
        self.filepath = filepath
        self.df = pd.read_csv(self.filepath,header = None)
        self.df.columns = ['VehicleType','DerectionTime_O','GantrylD_O',
              'DerectionTime_D','GantrylD_D','TripLength',
              'TripEnd','TripInformation']
        self.searchcolumns = searchcolumns
        self.searchkeywords = searchkeywords
        
        
        
    def search(self):
        search_df = copy.deepcopy(self.df)
        search_columns = copy.deepcopy(self.searchcolumns)
        search_keywords = copy.deepcopy(self.searchkeywords)
    # no keywords
        if search_keywords==['','']:
            return search_df
        # only 1 keyword
        elif '' in search_keywords:
            if search_keywords[0]=='':
                column,keyword = search_columns[1],search_keywords[1]
            else:
                column,keyword = search_columns[0],search_keywords[0]
            # fuzzy match
            if column in ['DerectionTime_O','DerectionTime_D','TripInformation']:
                return search_df[search_df[column].astype(str).str.contains(keyword)].reset_index(drop=True)
            else:
                # exact match
                return search_df[search_df[column].isin([keyword])].reset_index(drop=True)
        # 2 keywords    
        else:
            if search_columns[0]==search_columns[1]:
                # return an arange
                if search_columns[0] in ['DerectionTime_O','DerectionTime_D','TripLength']:
                    if search_columns[0]=='TripLength':
                        return search_df[search_df[search_columns[0]].between(float(min(search_keywords)),float(max(search_keywords)))].reset_index(drop=True)
                    # str to datetime to str
                    search_keywords = [str(pd.to_datetime(search_keywords)[i]) for i in [0,1]]
                    return search_df[search_df[search_columns[0]].between(min(search_keywords),max(search_keywords))].reset_index(drop=True)
                
                elif search_columns[0] in ['VehicleType','GantrylD_O','GantrylD_D','TripEnd']:
                     # exact match
                    return search_df[search_df[search_columns[0]].isin(search_keywords)].reset_index(drop=True)
                else:
                    # fuzzy match 
                    return search_df[(search_df[search_columns[0]].astype(str).str.contains(search_keywords[0]))
                              &(search_df[search_columns[1]].astype(str).str.contains(search_keywords[1]))].reset_index(drop=True)
            else:
                length = len(set(search_columns)&(set(['DerectionTime_O','DerectionTime_D','TripInformation'])))
                if length==2:
                    # fuzzy match
                    return search_df[(search_df[search_columns[0]].astype(str).str.contains(search_keywords[0]))
                              &(search_df[search_columns[1]].astype(str).str.contains(search_keywords[1]))].reset_index(drop=True)
                elif length==1:
                    # fuzzy match with exact match
                    if search_columns[0] in ['DerectionTime_O','DerectionTime_D','TripInformation']:
                        return search_df[(search_df[search_columns[0]].astype(str).str.contains(search_keywords[0]))
                                  &(search_df[search_columns[1]].isin([search_keywords[1]]))].reset_index(drop=True)
                    else:
                        return search_df[(search_df[search_columns[1]].astype(str).str.contains(search_keywords[1]))
                                  &(search_df[search_columns[0]].isin([search_keywords[0]]))].reset_index(drop=True)
                else:
                    # exact match
                    return search_df[(search_df[search_columns[0]].isin([search_keywords[0]]))&(search_df[search_columns[1]].isin([search_keywords[1]]))].reset_index(drop=True)


# test for class
a = Traffic_inquiry(filepath,['GantrylD_D','TripEnd'],['03F1991S','Y'])
b = a.search()  
