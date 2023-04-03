#!/usr/bin/env python
# coding: utf-8

# In[5]:


import os
import csv
import pandas as pd
import PySimpleGUI as sg
import logging

for filename in os.scandir():
    try:
        if filename.path.endswith(".csv"):
            df = pd.read_csv(filename.path)
            print(df)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            #overwrites to csv
            df.to_csv(filename.path, index=False)
            print("Done: "+ filename.name)
    except Exception as e:
        print(str(e) +" : " +filename.name)
        pass


input("Press any key to exit")


# In[ ]:




