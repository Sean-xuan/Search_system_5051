import pandas as pd
import numpy as np
import datetime as dt
from dateutil.parser import parse
import copy
import os
import time
import tkinter as tk
from tkinter import *
from tkinter import filedialog


class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.files = [('CSV Files', '*.csv*')]
        self.searchcolumns = ['', '']
        self.searchkeywords = ['', '']
        searchflag = 0

    def search(self):
        self.searchkeywords[0] = self.search_entry1.get()
        self.searchkeywords[1] = self.search_entry2.get()
        self.text1.delete(0.0, END)
        self.res = self.searchdf()
        searchflag = 1
        self.sortdf = self.res
        if searchflag == 1:
            self.text1.insert(INSERT, self.res)

    def searchdf(self):
        search_df = copy.deepcopy(self.df)
        search_columns = copy.deepcopy(self.searchcolumns)
        search_keywords = copy.deepcopy(self.searchkeywords)
        # no keywords
        if search_keywords == ['', '']:
            self.res=search_df
            return search_df
        # only 1 keyword
        elif '' in search_keywords:
            if search_keywords[0] == '':
                column, keyword = search_columns[1], search_keywords[1]
            else:
                column, keyword = search_columns[0], search_keywords[0]
            # fuzzy match
            if column in ['DerectionTime_O', 'DerectionTime_D']:
                pa=str(pd.to_datetime(keyword))
                self.res = search_df[search_df[column].astype(str).str.contains(str(pd.to_datetime(keyword)))].reset_index(drop=True)
                #temp=search_df[search_df[column].astype(str).str.contains(keyword)]
                #p(rint('!!!!!!!!', res)
                return self.res
            elif column in ['TripInformation']:
                self.res = search_df[search_df[column].astype(str).str.contains(keyword)].reset_index(drop=True)
                return self.res
            else:
                # exact match
                self.res = search_df[search_df[column].isin([keyword])].reset_index(drop=True)
                return self.res
        # 2 keywords
        else:
            if search_columns[0] == search_columns[1]:
                # return an arange
                if search_columns[0] in ['DerectionTime_O', 'DerectionTime_D', 'TripLength']:
                    if search_columns[0] == 'TripLength':
                        self.res = search_df[search_df[search_columns[0]].between(float(min(search_keywords)),
                                                                             float(max(search_keywords)))].reset_index(
                            drop=True)
                        return self.res
                    # str to datetime to str
                    search_keywords = [str(pd.to_datetime(search_keywords)[i]) for i in [0, 1]]
                    self.res = search_df[
                        search_df[search_columns[0]].between(min(search_keywords), max(search_keywords))].reset_index(
                        drop=True)
                    #return self.searchres
                elif search_columns[0] in ['VehicleType', 'GantrylD_O', 'GantrylD_D', 'TripEnd']:
                    # exact match
                    self.res = search_df[search_df[search_columns[0]].isin(search_keywords)].reset_index(drop=True)
                    #return self.searchres
                else:
                    # fuzzy match
                    self.res = search_df[(search_df[search_columns[0]].astype(str).str.contains(search_keywords[0]))
                                    & (search_df[search_columns[1]].astype(str).str.contains(
                        search_keywords[1]))].reset_index(drop=True)
            else:
                length = len(set(search_columns) & (set(['DerectionTime_O', 'DerectionTime_D', 'TripInformation'])))
                if length == 2:
                    # fuzzy match
                    self.res = search_df[(search_df[search_columns[0]].astype(str).str.contains(search_keywords[0]))
                                    & (search_df[search_columns[1]].astype(str).str.contains(
                        search_keywords[1]))].reset_index(drop=True)
                    #return res
                elif length == 1:
                    # fuzzy match with exact match
                    if search_columns[0] in ['DerectionTime_O', 'DerectionTime_D', 'TripInformation']:
                        self.res = search_df[(search_df[search_columns[0]].astype(str).str.contains(search_keywords[0]))
                                        & (search_df[search_columns[1]].isin([search_keywords[1]]))].reset_index(
                            drop=True)
                    else:
                        self.res = search_df[(search_df[search_columns[1]].astype(str).str.contains(search_keywords[1]))
                                        & (search_df[search_columns[0]].isin([search_keywords[0]]))].reset_index(
                            drop=True)
                else:
                    # exact match
                    self.res = search_df[(search_df[search_columns[0]].isin([search_keywords[0]])) & (
                        search_df[search_columns[1]].isin([search_keywords[1]]))].reset_index(drop=True)

    def tup(self,array):
        tups = []
        for i in range(len(array)):
            tups.append((array[i],i))
        return tups

    def quicksort(self,tups):
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
        m = self.quicksort(left)+[tups[0]]+self.quicksort(right)
        return m

    def sort(self):
        self.sortcolumn=self.ddb_sort1.get()
        values=['Ascending', 'Descending']
        self.signal = values.index(self.ddb_sort2.get())
        d = self.tup(self.sortdf[self.sortcolumn])
        b_in = np.array(self.quicksort(d))[:,1]
        a_in = [int(i) for i in b_in]
        a_de = list(reversed(a_in))
        if self.signal == 0:
            self.res=self.res.reindex(a_in)
        if self.signal == 1:
            self.res=self.res.reindex(a_de)
        self.text1.delete(0.0, END)
        self.text1.insert(INSERT, self.res)

    # init_window
    def set_init_window(self):
        self.init_window_name.title("Inquiry System for Traffic Data")
        self.init_window_name.geometry('900x581+10+10')
        self.init_data_label = Label(self.init_window_name, font=('Times New Roman', 12, 'bold'),
                                     text="Start from select file, ends with save file")
        self.init_data_label.place(x=300, y=5)
        self.str_trans_to_md1_button = Button(self.init_window_name, text='OPEN FILE', bg="lightblue",
                                              command=self.import_csv_data)
        self.str_trans_to_md1_button.grid(row=3, column=4)
        self.str_trans_to_md1_button.place(x=200, y=40)
        self.v = tk.StringVar()
        self.str_trans_to_md2_button = Button(self.init_window_name, text="SAVE FILE", bg="lightblue",
                                              command=self.savefile)
        self.str_trans_to_md2_button.place(x=600, y=40)
        # show df
        self.text1 = Text(self.init_window_name, width=140, height=10, bg="white",
                          font=('Helvetica', '8'))  # other option
        self.text1.place(x=10, y=100)

    def set_later_window(self):
        # sort
        self.x0, self.y0 = 450, 260
        self.sort_lable = Label(self.init_window_name, text='Sort', font=('Helvetican', 18, 'bold'))
        self.sort_lable.place(x=self.x0, y=self.y0)
        self.sort_lable1 = Label(self.init_window_name, text='Choose a cloumn')
        self.sort_lable1.place(x=self.x0, y=self.y0 + 60)
        self.ddb_sort1_L = Label(self.init_window_name, text='Columns')
        self.ddb_sort1 = ttk.Combobox(self.init_window_name, values=['VehicleType', 'DerectionTime_O', 'GantrylD_O',
                           'DerectionTime_D', 'GantrylD_D', 'TripLength','TripEnd'])
        self.ddb_sort1.place(x=self.x0 + 150, y=self.y0 + 60)
        self.ddb_sort1.current(1)

        self.sort_lable2 = Label(self.init_window_name, text='Ascending?')
        self.sort_lable2.place(x=self.x0, y=self.y0 + 100)
        self.ddb_sort2 = ttk.Combobox(self.init_window_name, values=['Ascending', 'Descending'])
        self.ddb_sort2.place(x=self.x0 + 150, y=self.y0 + 100)
        self.ddb_sort2.current(1)
        # sort bottom
        self.sort_button = Button(self.init_window_name, text='SORT', bg="lightblue", command=self.sort)
        self.sort_button.place(x=self.x0 + 150, y=self.y0)

        # search title
        self.x1, self.y1 = 30, 260
        self.search_lable = Label(self.init_window_name, text='Search', font=('Helvetican', 18, 'bold'))
        self.search_lable.place(x=self.x1, y=self.y1)
        # search 1
        self.search_lable1 = Label(self.init_window_name, text='Choose 1st cloumn')
        self.search_lable1.place(x=self.x1, y=self.y1 + 60)
        self.ddb_search1 = ttk.Combobox(self.init_window_name, values=self.columns)
        self.ddb_search1.place(x=self.x1 + 150, y=self.y1 + 60)
        self.ddb_search1.current(1)
        self.ddb_search1.bind("<<ComboboxSelected>>", self.callbackFunc)
        self.search_lable1 = Label(self.init_window_name, text='Keyword')
        self.search_lable1.place(x=self.x1, y=self.y1 + 100)
        self.search_entry1 = tk.Entry(self.init_window_name, width=22)
        self.search_entry1.place(x=self.x1 + 150, y=self.y1 + 100)
        self.search_lable2 = Label(self.init_window_name, text='Input example')
        self.search_lable2.place(x=self.x1, y=self.y1 + 120)
        # search 2
        self.search_lable2 = Label(self.init_window_name, text='Choose 2nd cloumn')
        self.search_lable2.place(x=self.x1, y=self.y1 + 160)
        self.ddb_search2 = ttk.Combobox(self.init_window_name, values=self.columns)
        self.ddb_search2.place(x=self.x1 + 150, y=self.y1 + 160)
        self.ddb_search2.current(1)
        self.ddb_search2.bind("<<ComboboxSelected>>", self.callbackFunc2)
        self.search_lable2 = Label(self.init_window_name, text='Keyword')
        self.search_lable2.place(x=self.x1, y=self.y1 + 200)
        self.search_entry2 = tk.Entry(self.init_window_name, width=22)
        self.search_entry2.place(x=self.x1 + 150, y=self.y1 + 200)
        self.search_lable2 = Label(self.init_window_name, text='Input example')
        self.search_lable2.place(x=self.x1, y=self.y1 + 220)

        # search bottom
        self.search_button = Button(self.init_window_name, text='SEARCH', bg="lightblue", command=self.search)
        self.search_button.place(x=self.x1 + 160, y=self.y1)

    def callbackFunc(self, event):
        self.get1 = self.ddb_search1.get()
        self.searchcolumns[0] = self.get1
        self.ddb_search1.pack_forget()
        self.get1 = self.ddb_search1.get()
        info1 = self.df[self.get1][1]
        self.search_info1 = Label(self.init_window_name, text=info1, bg="lightblue", width=22)
        self.search_info1.place(x=self.x1 + 150, y=self.y1 + 120)

    def callbackFunc2(self, event):
        self.get2 = self.ddb_search2.get()
        self.searchcolumns[1] = self.get2
        self.ddb_search2.pack_forget()
        info2 = self.df[self.get2][1]
        self.search_info2 = Label(self.init_window_name, text=info2, bg="lightblue", width=22)
        self.search_info2.place(x=self.x1 + 150, y=self.y1 + 220)

    def import_csv_data(self):
        global v
        pd.set_option('display.width', 5000)
        ###csv_file_path = filedialog.askopenfilename(filetypes = self.files, defaultextension = self.files)
        csv_file_path = 'C:/Users/hp/Desktop/HOMEWORK/5051/data/date.csv'
        print(csv_file_path)
        self.df = pd.read_csv(csv_file_path, header=None)
        self.res = self.df
        self.df.columns = ['VehicleType', 'DerectionTime_O', 'GantrylD_O',
                           'DerectionTime_D', 'GantrylD_D', 'TripLength',
                           'TripEnd', 'TripInformation']
        self.columns = self.df.columns.tolist()
        self.text1.insert(INSERT, self.df[:10])
        self.set_later_window()

    def savefile(self):
        dlg = filedialog.asksaveasfilename()
        filepath = os.path.abspath(dlg)
        print(filepath)
        self.res.to_csv(filepath)

    def quit():
        root.destroy()


def gui_start():
    init_window = Tk()  
    ZMJ_PORTAL = MY_GUI(init_window)
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop() 

if __name__=="__main__":
    gui_start()
