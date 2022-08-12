#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import csv
import math
import pandas as pd
import PySimpleGUI as sg
import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG, format='%(message)s')
#ask for user input
sg.theme('SandyBeach')
layout = [
    [sg.Text('Which sheet and column would you like to work with?')],
    [sg.Text('Column Name', size =(15, 1)), sg.InputText()],
    #[sg.Text('Sheet Number', size =(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('Simple data entry window', layout)
event, values = window.read()
window.close()

#sheetNumber=values[1]
columnName=values[0]

for folderName in os.scandir():
    if folderName.is_dir():
        print(folderName)
        logging.info(folderName)
        for filename in os.scandir(folderName):
            try:
                if filename.path.endswith(".csv"):
                    overWriteColumn=[]
                    df = pd.read_csv(filename.path)
                    toOverwrite= df[columnName]
                    for unrounded in toOverwrite:
                        print(str(unrounded) + " rounded to "+ str(round(float(unrounded),6)))
                        logging.info(str(unrounded) + " rounded to "+ str(round(float(unrounded),6)))
                        overWriteColumn.append(round(float(unrounded),6))
                    df[columnName]=overWriteColumn
                    df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
                    df.to_csv(filename.path, index=False)
                    print("Done: "+ filename.name)
                    logging.info("Done: "+ filename.name)
            except Exception as e:
                print(str(e)+ " : " +filename.name)
                logging.info(str(e)+ " : " +filename.name)
                pass

input("Press any key to exit")


# In[ ]:




