#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import csv
import pandas as pd
import PySimpleGUI as sg
import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG, format='%(message)s')

sg.theme('SandyBeach')
layout = [
    [sg.Text('How many normalization columns would you like to add?')],
    [sg.Text('Number of times', size =(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('Simple data entry window', layout)
event, values = window.read()
window.close()


numTimes=int(values[0])
counter=0

while counter<numTimes:
    sg.theme('SandyBeach')
    layout = [
        [sg.Text('Please enter reference m/z, C13, numerator, and name for new column')],
        [sg.Text('Reference m/z', size =(15, 1)), sg.InputText()],
        [sg.Text('Column Name', size =(15, 1)), sg.InputText()],
        [sg.Text('C13', size =(15, 1)), sg.InputText()],
        [sg.Text('Numerator Column', size =(15, 1)), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('Simple data entry window', layout)
    event, values = window.read()
    window.close()

    refNum=float(values[0])
    newColumnHeader=values[1]
    C13Value=int(values[2])
    numColumn=values[3]

    print("Numerator column is " + numColumn)
    print("Using reference m/z of " + str(refNum))
    print("New Column Name is "+ newColumnHeader)
    logging.info("Using reference m/z of " + str(refNum))
    logging.info("New Column Name is "+ newColumnHeader)
    
    for folderName in os.scandir():
        if folderName.is_dir():
            print(folderName)
            for filename in os.scandir(folderName):
                try:
                    if filename.path.endswith(".csv"):
                        df = pd.read_csv(filename.path)
                        #extracts denominator using refNum and 13C==0 
                        denominator=df.loc[(df['Ref m/z'] == refNum) & (df["13C"]==C13Value)]["Corrected Intensity"].iloc[0]
                        #dividing everything and adding to column
                        addColumn=[]
                        numerators= df[numColumn]
                        for num in numerators:
                            addColumn.append(num/denominator)
                        df[newColumnHeader]=addColumn
                        #overwrites to csv
                        df.to_csv(filename.path, index=False)
                    print("Done: "+ filename.name)
                    logging.info("Done: "+ filename.name)
                except Exception as e:
                    print(str(e) +" : " +filename.name)
                    logging.info(str(e) +" : " +filename.name)
                    pass
    
    counter+=1

input("Press any key to exit")


# In[ ]:




