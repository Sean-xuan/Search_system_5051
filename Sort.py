# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 14:14:07 2022

@author: brynn
"""

import pandas as pd
import numpy as np
import datetime as dt
from dateutil.parser import parse
import copy

'''
signal = 0: 升序排序
signal = 1: 降序排序
直接使用 sort(df,columns，signal)函数
'''

df = pd.read_csv('TDCS_M06A_20190830_080000.csv',header = None)

def tup(array):
    tup = []
    for i in range(len(array)):
        tup.append((array[i],i))
    return tup
def quicksort(tups):
    judge = []
    for i in tups:
        judge.append(i[0])

    if len(set(judge)) < 2:
        return tups
    pivot = tups[0][0]
    left = []
    for i in tups[1:]:
        if i[0] <= pivot:
            left.append(i)
    right = []
    for i in tups[1:]:
        if i[0] > pivot:
            right.append(i)
    m = quicksort(left)+[tups[0]]+quicksort(right)
    return m



def sort(df,columns,signal):
    
    d = tup(df[columns])
    b_in = np.array(quicksort(d))[:,1]
    a_in = [int(i) for i in b_in]
    a_de = list(reversed(a_in))

    if signal == 0:
        return df.reindex(a_in)
    if signal == 1:
        return df.reindex(a_de)

    
##test:
x = sort(df,6,1)

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
