#!/usr/bin/env python
# coding: utf-8

# In[40]:


import os
import csv
import pandas as pd
import PySimpleGUI as sg
import logging

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

logging.basicConfig(filename='example.log', level=logging.DEBUG, format='%(message)s')
#pop up to ask for sheet number
sg.theme('SandyBeach')
layout = [
    [sg.Text('Which sheet number would you like to work with?')],
    [sg.Text('Sheet Number', size =(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('Simple data entry window', layout)
event, values = window.read()
window.close()

sheetNumber=values[0]
#sheetNumber=5
        

#searches for excel file 
for excel in os.scandir():
    if excel.path.endswith(".xlsx"):
        print("Excel: " + excel.name)
        logging.info("Excel: " + excel.name)
        xls = pd.ExcelFile(excel)
        excelDF = pd.read_excel(xls, sheet_name=int(sheetNumber)-1)

#pop up to ask for column names of excel        
sg.theme('SandyBeach')
layout = [
    [sg.Text('What are the column names?')],
    [sg.Text('ID column name', size =(15, 1)), sg.InputText()],
    [sg.Text('Normalization (denominator) name', size =(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('Simple data entry window', layout)
event, values = window.read()
window.close()
        
IDCol=values[0]
denominatorCol=values[1]

#IDCol="ID"
#denominatorCol="BCA protein (ug)"

#extracting denom and id and storing it into arrays
IDArray=excelDF.loc[:, [IDCol]].values
cleanIDArray=[]
for ID in IDArray:
    cleanIDArray.append(str(ID[0]))

denominatorArray=excelDF.loc[:, [denominatorCol]].values
cleanDenomArray=[]
for denom in denominatorArray:
    cleanDenomArray.append(denom[0])
    
#asking for column name in excel files
sg.theme('SandyBeach')
layout = [
    [sg.Text('What is the column name for the numerator?')],
    [sg.Text('What is the new column name to be added?')],
    [sg.Text('Numerator column name', size =(15, 1)), sg.InputText()],
    [sg.Text('New column name', size =(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('Simple data entry window', layout)
event, values = window.read()
window.close()

numColumn=values[0]
#numColumn="rel to d7"
newColumnHeader=values[1]
#newColumnHeader="ProteinNorm"

#looping through the two arrays and writing to csv
counter=0
while counter<len(cleanIDArray):
    isFound=False 
    for folder in os.scandir():
        if folder.is_dir(): #goes into every folder
            for filename in os.scandir(folder):
                if str(cleanIDArray[counter]) in filename.name and filename.path.endswith(".csv"):
                    isFound=True
                    #open up and modify csv file
                    try:
                        df = pd.read_csv(filename.path)
                        addColumn=[]
                        numerators= df[numColumn]
                        for num in numerators:
                            addColumn.append(num/cleanDenomArray[counter])
                        df[newColumnHeader]=addColumn
                        print(str(cleanIDArray[counter])+ " : "+ filename.name)
                        logging.info(str(cleanIDArray[counter])+ " : "+ filename.name)
                        df.to_csv(filename.path, index=False)
                    except Exception as e:
                        print(str(e))
                        logging.info(str(e))
    
    
    if isFound==False:
        print("CSV not found for specific protein: " + str(cleanIDArray[counter]))
        logging.info("CSV not found for specific protein: " + str(cleanIDArray[counter]))
    counter+=1


#checking for missing protein using csv
print("Now checking for missing IDs")
logging.info("Now checking for missing IDs")
for folderName in os.scandir():
    if folderName.is_dir():
        print(folderName.name)
        for csvName in os.scandir(folderName):
            findthisID=csvName.name[find_nth(csvName.name,"_",4)+1:find_nth(csvName.name,".csv",1)]
            if findthisID in cleanIDArray:
                print("Found in ID List: "+ findthisID)
                logging.info("Found in ID List: "+ findthisID)
            else:
                print("Not found in ID List: "+ findthisID)
                logging.info("Not found in ID List: "+ findthisID)

input("Press any key to exit")


# In[ ]:




