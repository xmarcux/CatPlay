#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

class SettingsDialog(wx.Dialog):
    """
    This class is a dialog
    to change settings for 
    the application.
    It is opened from Tools->Settings... menu
    """

    def __init__(self, *args, **kw):
        """Initialization."""

        super(SettingsDialog, self).__init__(*args, **kw)

        self.SetTitle(_('Settings'))
        self.__createView()

    def __createView(self):
        """Method creates the view of the dialog."""

        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        labelSizer = wx.BoxSizer(wx.VERTICAL)
        #inputSizer = wx.BoxSizer(wx.VERTICAL)
        #actionSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(labelSizer, 0, wx.ALL | wx.EXPAND, 5)
        #topSizer.Add(inputSizer, 0, wx.ALL | wx.EXPAND, 5)
        #topSizer.Add(actionSizer, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(topSizer, 0, wx.ALL | wx.EXPAND, 5)

        #File path
        filePathLbl = wx.StaticText(panel, wx.ID_ANY, _('Filepath to music base file directory:'))
        labelSizer.Add(filePathLbl, 0, wx.ALL, 1)
        fileInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        labelSizer.Add(fileInputSizer, 1, wx.ALL | wx.EXPAND, 5)
        self.__fileInput = wx.TextCtrl(panel, wx.ID_ANY)
        fileInputSizer.Add(self.__fileInput, 1, wx.ALL | wx.EXPAND, 5)
        browseBtn = wx.Button(panel, wx.ID_ANY, _('&Browse...'))
        self.Bind(wx.EVT_BUTTON, self.__onBrowse, browseBtn)
        fileInputSizer.Add(browseBtn, 0, wx.ALL, 5)
        
        #File separator
        sepSizer = wx.BoxSizer(wx.HORIZONTAL)
        labelSizer.Add(sepSizer, 1, wx.ALL, 5)
        separatorLbl = wx.StaticText(panel, wx.ID_ANY, 
                                     _('Filename separator between bpm, category and artist name/song title:'))
        sepSizer.Add(separatorLbl, 1, wx.ALL, 5)
        self.__separatorInput = wx.TextCtrl(panel, wx.ID_ANY)
        self.__separatorInput.SetMaxLength(1)
        sepSizer.Add(self.__separatorInput, 0, wx.ALL | wx.EXPAND, 5)

        #Buttons
        labelSizer.Add(wx.StaticLine(panel, wx.ID_ANY), 0, wx.ALL | wx.EXPAND, 5)
        saveBtn = wx.Button(panel, wx.ID_ANY, _('&Save'))
        self.Bind(wx.EVT_BUTTON, self.__onSave, saveBtn)
        cancelBtn = wx.Button(panel, wx.ID_ANY, _('&Cancel'))
        self.Bind(wx.EVT_BUTTON, self.__onCancel, cancelBtn)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(saveBtn, 0, wx.ALL, 5)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)
        mainSizer.Add(btnSizer, 0, wx.BOTTOM | wx.ALIGN_CENTER, 5)

        """ make own dialog
        addCategoryLbl = wx.StaticText(panel, wx.ID_ANY, _('Add category name:'))
        labelSizer.Add(addCategoryLbl, 1, wx.ALL, 5)
        addCatTokenLbl = wx.StaticText(panel, wx.ID_ANY, 
                                       _('Character in filename representing category:'))
        labelSizer.Add(addCatTokenLbl, 1, wx.ALL, 5)
        """

        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

    def __onBrowse(self, event):
        """Browse button clicked."""

        fileDialog = wx.DirDialog(self, _('Choose music base file directory:'))
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return
                                
        self.__fileInput.SetValue(fileDialog.GetPath())

    
    def __onSave(self, event):
        """Save button clicked."""

        print('Saving')
        self.Destroy()


    def __onCancel(self, event):
       """Cancel button clicked."""
       self.Destroy()
