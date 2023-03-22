#!/usr/bin/env python
# coding: utf-8

# In[7]:


import wx
import wx.lib.agw.genericmessagedialog as GMD
import sys
import traceback
import pandas
import re
import glob

__version__ = "1.1.0"
__version_date__ = "November 04 2019"


def exception_handler(exc_type, exc_value, exc_traceback):
    """Handle unhandled exceptions so the user gets a dialog box with the error."""
        
    message = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    print(message)
    
    msg_dlg = wx.MessageDialog(None, message, "Unhandled Exception", wx.OK | wx.ICON_EXCLAMATION)
    msg_dlg.ShowModal()
    msg_dlg.Destroy()
    exit(1)


sys.excepthook = exception_handler




class Check_Duplicates_GUI(wx.Frame):
    
    
    def __init__(self, parent, title, *args, **kwargs):
        
        super(Check_Duplicates_GUI, self).__init__(parent, title=title, *args, **kwargs) 
            
        self.InitUI()
        self.Fit()
        self.Centre()
        self.Show()



    def InitUI(self):
        
        self.input_file_okay = False
 
        ##############
        ## Menu Bar
        ##############
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        
        ## Add items to file menu.
        open_item = fileMenu.Append(wx.ID_OPEN, "&Open", "Open CSV File")
        self.Bind(wx.EVT_MENU, self.OnOpen, open_item)
        
        about_item = fileMenu.Append(100, '&About   \tCtrl+A', 'Information about the program')
        self.Bind(wx.EVT_MENU, self.OnAbout, about_item)
        
        
        fileMenu.AppendSeparator()
        
        quit_item = wx.MenuItem(fileMenu, 101, 'Quit', 'Quit Application')
        fileMenu.Append(quit_item)
        self.Bind(wx.EVT_MENU, self.OnQuit, quit_item)
        
        
        ## Add file menu to the menu bar.
        menubar.Append(fileMenu, "&File")
        
        ## Put menu bar in frame.
        self.SetMenuBar(menubar)



        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)
        
        
        ##############
        ## Display File to Check
        ##############
        file_label = wx.StaticText(panel, label = "Current File:")
        self.current_file_st = wx.StaticText(panel)
        self.current_file_st.SetMinSize((450,30))
        
        vbox.Add(file_label, flag=wx.ALIGN_LEFT|wx.LEFT|wx.TOP, border=10)
        vbox.Add(self.current_file_st, flag=wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, border=10, proportion=0)
        
        
        ##############
        ## Columns For Unique ID
        ##############
        column_select_label = wx.StaticText(panel, label = "Unique ID Columns:")
        
        self.columns_listbox = wx.CheckListBox(panel)
        self.columns_listbox.SetMinSize((250,400))
        
        vbox.Add(column_select_label, flag=wx.ALIGN_LEFT|wx.LEFT|wx.TOP|wx.EXPAND, border=10)
        vbox.Add(self.columns_listbox, flag=wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, border=10, proportion=1)
        
        
        
        ##############
        ## Buttons
        ##############
        
        run_button = wx.Button(panel, label = "Run")
        run_button.Bind(wx.EVT_BUTTON, self.OnRun)

        vbox.Add(run_button, flag = wx.ALIGN_CENTER|wx.ALL, border = 10)
        
        panel.SetSizer(vbox)
        panel.Fit()




    def OnAbout(self, event):
        message = "Author: Travis Thompson \n\n" +         "Creation Date: September 2019 \n" +         "Version Number: " + __version__ +         "Version Date: " + __version_date__
       
        dlg = GMD.GenericMessageDialog(None, message, "About", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
        
        
        
        
    def OnQuit(self, e):
        self.Close()
        
        
        
    
    def set_unique_columns(self, columns):
        self.columns_listbox.Clear()
        self.columns_listbox.Set(list(columns))
        
        ECF_columns = ["sample ID", "amino acids", "adduct", "2H", "15N", "13C"]
        lipids_columns = ["Lipid class", "Acyl Chain", "Unsat sites", "Mol Formula", "13C", "Attribute (database result)"]
        
        ECF_matches = set(columns).intersection(set(ECF_columns))
        lipids_matches = set(columns).intersection(set(lipids_columns))
        if len(ECF_matches) > len(lipids_matches):
            self.columns_listbox.SetCheckedStrings(ECF_matches)
            
        elif len(lipids_matches) > 0:
            self.columns_listbox.SetCheckedStrings(lipids_matches)



    
    def OnOpen(self, event):
        input_file_okay = self.input_file_okay
        
        ## Get file from user.
        dlg = wx.FileDialog(self, message = "Select CSV File", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            file_path = dlg.GetPath()
            dlg.Destroy()
        else:
            dlg.Destroy()
            self.input_file_okay = input_file_okay
            return
      
        ## Make sure it is a CSV file.
        if not re.match(r".*\.csv", file_path):
            message = "The selected file is not a CSV file."
            msg_dlg = wx.MessageDialog(None, message, "Warning", wx.OK | wx.ICON_EXCLAMATION)
            msg_dlg.ShowModal()
            msg_dlg.Destroy()
            self.input_file_okay = input_file_okay
            return
        
        
        working_df = pandas.read_csv(file_path)
        self.set_unique_columns(working_df.columns)

        
        
        self.input_file_okay = True
        self.file_path = file_path
        self.current_file_st.SetLabel(file_path)
        self.working_df = working_df
        global filePathEY,selectedFilePathEY
        selectedFilePathEY=file_path
        
        filePathEY=glob.glob('*.csv')
        
        
        
        
    def OnRun(self, event):
        
        if not self.input_file_okay:
            message = "Please select a file."
            msg_dlg = wx.MessageDialog(None, message, "Warning", wx.OK | wx.ICON_EXCLAMATION)
            msg_dlg.ShowModal()
            msg_dlg.Destroy()
            return
        
        
        unique_ID_columns = self.columns_listbox.GetCheckedStrings()
        if len(unique_ID_columns) <= 0:
            message = "Please select at least one column as a unique ID."
            msg_dlg = wx.MessageDialog(None, message, "Warning", wx.OK | wx.ICON_EXCLAMATION)
            msg_dlg.ShowModal()
            msg_dlg.Destroy()
            return
        
        
        self.working_df.loc[:, "Duplicated"] = self.working_df.duplicated(subset = unique_ID_columns, keep=False)
        value_counts = self.working_df.loc[:, "Duplicated"].value_counts()
        if True in value_counts.index:
            number_of_duplicates = value_counts[True]
            message = "There are " + str(number_of_duplicates) + " duplicates in the input data set. Click Okay to save the data with a column marking the duplicates."
            msg_dlg = wx.MessageDialog(None, message, "Duplicates Detected", wx.OK|wx.CANCEL)
            
            if msg_dlg.ShowModal() == wx.ID_OK:
                msg_dlg.Destroy()
                
                        
                self.working_df.to_csv(selectedFilePathEY, index=False)
                
            else:
                msg_dlg.Destroy()
                return
            
        else:
            message = "No duplicates were found in the data."
            msg_dlg = wx.MessageDialog(None, message, "No Duplicates Found", wx.OK)
            msg_dlg.ShowModal()
            msg_dlg.Destroy()
            return
        
        ###evan edits
        for csv in filePathEY:
            working_df = pandas.read_csv(csv)
            self.set_unique_columns(working_df.columns)
            
            #self.input_file_okay = True
            self.file_path = csv
            #self.current_file_st.SetLabel(file_path)
            self.working_df = working_df
            
            #change self.working_df.loc value below
            self.working_df.loc[:, "Duplicated"] = self.working_df.duplicated(subset = unique_ID_columns, keep=False)
            value_counts = self.working_df.loc[:, "Duplicated"].value_counts()
            if True in value_counts.index:
                number_of_duplicates = value_counts[True]
                #message = "There are " + str(number_of_duplicates) + " duplicates in the input data set. Click Okay to save the data with a column marking the duplicates."
                #msg_dlg = wx.MessageDialog(None, message, "Duplicates Detected", wx.OK|wx.CANCEL)
            
                #if msg_dlg.ShowModal() == wx.ID_OK:
                 #   msg_dlg.Destroy()
                
                    #change variable name below
                self.working_df.to_csv(csv, index=False)
                
               # else:
                #    msg_dlg.Destroy()
                 #   return
            
            else:
                message = "No duplicates were found in the data."
                msg_dlg = wx.MessageDialog(None, message, "No Duplicates Found", wx.OK)
                msg_dlg.ShowModal()
                msg_dlg.Destroy()
                return
            
        
        



def main():
    ex = wx.App(False)
    Check_Duplicates_GUI(None, title = "Check For Duplicates")
    ex.MainLoop()    


if __name__ == '__main__':
    main()


