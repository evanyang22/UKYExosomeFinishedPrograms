#!/usr/bin/env python
# coding: utf-8

# In[20]:


import os
import csv
import pandas as pd
import PySimpleGUI as sg
import logging

sg.theme('SandyBeach')
layout = [
    [sg.Text('How many columns would you like to keep?')],
    [sg.Text('Amount of Columns', size =(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('Simple data entry window', layout)
event, values = window.read()
window.close()

for filename in os.scandir():
    try:
        if filename.path.endswith(".csv"):
            #df = pd.read_csv(filename.path, error_bad_lines=False,engine="python")
            df = pd.read_csv(filename.path,engine="python",usecols=range(0, int(values[0])))
            
            #overwrites to csv
            df.to_csv(filename.path, index=False)
            print("Done: "+ filename.name)
    except Exception as e:
        print(str(e) +" : " +filename.name)
        pass


#input("Press any key to exit")


# In[ ]:




