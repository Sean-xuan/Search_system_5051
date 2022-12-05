import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import *
from tkinter import filedialog

import hashlib
import time
import pandas as pd
import os
from tkinter import ttk
import copy

class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.files = [('CSV Files', '*.csv*')]
        self.searchcolumns = ['', '']
        self.searchkeywords = ['', '']
        searchflag = 0
        # self.v= StringVar()

    def search(self):
        self.searchkeywords[0] = self.search_entry1.get()
        self.searchkeywords[1] = self.search_entry2.get()
        self.text1.delete(0.0, END)
        self.searchres = self.searchdf()
        searchflag = 1
        if searchflag == 1:
            print(self.searchkeywords)
            print(self.searchcolumns)
            print('start!!!1', self.searchres)

            # self.searchtext1 = Text(self.init_window_name,width=140,height=10,bg="white",font=('Helvetica', '8')) # other option
            # self.searchtext1.place(x=10, y=100)
            self.text1.insert(INSERT, self.searchres)

    def searchdf(self):
        search_df = copy.deepcopy(self.df)
        search_columns = copy.deepcopy(self.searchcolumns)
        search_keywords = copy.deepcopy(self.searchkeywords)
        print('!!!!!!!!', search_df, search_columns)
        # no keywords
        if search_keywords == ['', '']:
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
                self.searchres = search_df[search_df[column].astype(str).str.contains(str(pd.to_datetime(keyword)))].reset_index(drop=True)
                #temp=search_df[search_df[column].astype(str).str.contains(keyword)]
                #p(rint('!!!!!!!!', res)
                return self.searchres
            elif column in ['TripInformation']:
                self.searchres = search_df[search_df[column].astype(str).str.contains(keyword)].reset_index(drop=True)
                return self.searchres
            else:
                # exact match
                self.searchres = search_df[search_df[column].isin([keyword])].reset_index(drop=True)
                #print('!!!!!!!!', search_df[search_df[column].isin([keyword])].reset_index(drop=True))
                return self.searchres
        # 2 keywords
        else:
            if search_columns[0] == search_columns[1]:
                # return an arange
                if search_columns[0] in ['DerectionTime_O', 'DerectionTime_D', 'TripLength']:
                    if search_columns[0] == 'TripLength':
                        self.searchres = search_df[search_df[search_columns[0]].between(float(min(search_keywords)),
                                                                             float(max(search_keywords)))].reset_index(
                            drop=True)
                        print('!!!!!!!!', res)
                        return res
                    # str to datetime to str
                    search_keywords = [str(pd.to_datetime(search_keywords)[i]) for i in [0, 1]]
                    self.searchres = search_df[
                        search_df[search_columns[0]].between(min(search_keywords), max(search_keywords))].reset_index(
                        drop=True)
                    print('!!!!!!!!', res)
                    #return self.searchres
                elif search_columns[0] in ['VehicleType', 'GantrylD_O', 'GantrylD_D', 'TripEnd']:
                    # exact match
                    self.searchres = search_df[search_df[search_columns[0]].isin(search_keywords)].reset_index(drop=True)
                    print('!!!!!!!!', res)
                    #return self.searchres
                else:
                    # fuzzy match
                    self.searchres = search_df[(search_df[search_columns[0]].astype(str).str.contains(search_keywords[0]))
                                    & (search_df[search_columns[1]].astype(str).str.contains(
                        search_keywords[1]))].reset_index(drop=True)
                    print('!!!!!!!!', res)
                    #return res
            else:
                length = len(set(search_columns) & (set(['DerectionTime_O', 'DerectionTime_D', 'TripInformation'])))
                if length == 2:
                    # fuzzy match
                    self.searchres = search_df[(search_df[search_columns[0]].astype(str).str.contains(search_keywords[0]))
                                    & (search_df[search_columns[1]].astype(str).str.contains(
                        search_keywords[1]))].reset_index(drop=True)
                    print('!!!!!!!!', res)
                    #return res
                elif length == 1:
                    # fuzzy match with exact match
                    if search_columns[0] in ['DerectionTime_O', 'DerectionTime_D', 'TripInformation']:
                        self.searchres = search_df[(search_df[search_columns[0]].astype(str).str.contains(search_keywords[0]))
                                        & (search_df[search_columns[1]].isin([search_keywords[1]]))].reset_index(
                            drop=True)
                        print('!!!!!!!!', res)
                        #return
                    else:
                        self.searchres = search_df[(search_df[search_columns[1]].astype(str).str.contains(search_keywords[1]))
                                        & (search_df[search_columns[0]].isin([search_keywords[0]]))].reset_index(
                            drop=True)
                        print('!!!!!!!!', res)
                        #return res
                else:
                    # exact match
                    self.searchres = search_df[(search_df[search_columns[0]].isin([search_keywords[0]])) & (
                        search_df[search_columns[1]].isin([search_keywords[1]]))].reset_index(drop=True)
                    print('!!!!!!!!', res)
                    #return res

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("Inquiry System for Traffic Data")
        self.init_window_name.geometry('928x581+10+10')
        # self.init_window_name["bg"] = "MidnightBlue"                                    #窗口背景色
        # self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高

        self.init_data_label = Label(self.init_window_name, font=('Times New Roman', 12, 'bold'),
                                     text="Start from select file, ends with save file")
        # self.init_data_label.grid(row=0, column=8)
        self.init_data_label.place(x=100, y=5)

        self.str_trans_to_md1_button = Button(self.init_window_name, text='OPEN FILE', bg="lightblue",
                                              command=self.import_csv_data)
        # (, text="OPEN FILE",font=('Helvetica', '8'),bg="lightblue", width=8,command=lambda : self.openfile())  # 调用内部方法  加()为直接调用
        self.str_trans_to_md1_button.grid(row=3, column=4)
        self.str_trans_to_md1_button.place(x=50, y=40)
        self.v = tk.StringVar()
        self.str_trans_to_md2_button = Button(self.init_window_name, text="SAVE FILE", bg="lightblue",
                                              command=self.savefile)
        self.str_trans_to_md2_button.place(x=300, y=40)
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
        self.ddb_sort1 = ttk.Combobox(self.init_window_name, values=self.columns)
        self.ddb_sort1.place(x=self.x0 + 150, y=self.y0 + 60)
        self.ddb_sort1.current(1)
        self.get1 = self.ddb_sort1.get()
        self.ddb_sort1.bind("<<ComboboxSelected>>", self.callbackFunc)
        self.sort_lable2 = Label(self.init_window_name, text='Ascending?')
        self.sort_lable2.place(x=self.x0, y=self.y0 + 100)
        self.ddb_sort2 = ttk.Combobox(self.init_window_name, values=['Ascending', 'Descending'])
        self.ddb_sort2.place(x=self.x0 + 150, y=self.y0 + 100)
        self.ddb_sort2.current(1)
        self.get2 = self.ddb_sort2.get()
        # sort bottom
        self.sort_button = Button(self.init_window_name, text='SORT', bg="lightblue", command=self.import_csv_data)
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
        # self.search_entry1.pack()
        # self.search_entry1.bind("<<ComboboxSelected>>", self.keywordchange)
        # .bind("<Return>", self.keywordchange)

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

    # def keywordchange(self,event):

    def callbackFunc(self, event):

        self.get1 = self.ddb_search1.get()
        self.searchcolumns[0] = self.get1
        print("New Element Selected", self.get1, self.searchcolumns)
        self.ddb_search1.pack_forget()
        self.get1 = self.ddb_search1.get()
        info1 = self.df[self.get1][1]
        self.search_info1 = Label(self.init_window_name, text=info1, bg="lightblue", width=22)
        self.search_info1.place(x=self.x1 + 150, y=self.y1 + 120)

    def callbackFunc2(self, event):
        self.get2 = self.ddb_search2.get()
        self.searchcolumns[1] = self.get2
        print("New Element Selected", self.get2, self.searchcolumns)
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
        self.df.columns = ['VehicleType', 'DerectionTime_O', 'GantrylD_O',
                           'DerectionTime_D', 'GantrylD_D', 'TripLength',
                           'TripEnd', 'TripInformation']
        self.searchres = self.df[0:1]
        self.columns = self.df.columns.tolist()
        self.text1.insert(INSERT, self.df[:10])
        self.set_later_window()

    def savefile(self):
        # 获取文件夹路径
        global filepath
        global df
        dlg = filedialog.asksaveasfilename()
        filepath = os.path.abspath(dlg)
        print(filepath)
        data = pd.read_csv(str(filepath))
        self.df = pd.DataFrame(data)
        print('\n获取的文件地址：', filepath)
        print(self.df)
        return filepath

    def quit():
        root.destroy()


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()
