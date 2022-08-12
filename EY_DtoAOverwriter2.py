#!/usr/bin/env python
# coding: utf-8

# In[13]:


import os
import csv
import pandas as pd

for folderName in os.scandir():
    if folderName.is_dir():
        print(folderName)
        for filename in os.scandir(folderName):
            try:
                if filename.path.endswith(".csv"):
                    df = pd.read_csv(filename.path)
                    if "Corrected m/z" in df and "m/z" in df:
                        df["m/z"]=df["Corrected m/z"]
                    df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
                    df.to_csv(filename.path, index=False)
                    print("Done: "+ filename.name)
            except Exception as e:
                print(str(e)+ " : " +filename.name)
                pass

input("Press any key to exit")


# In[ ]:




