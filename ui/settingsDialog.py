#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os.path
import filectrl

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
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(labelSizer, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(topSizer, 0, wx.ALL | wx.EXPAND, 5)

        properties = filectrl.getProperties()

        #File path
        filePathLbl = wx.StaticText(panel, wx.ID_ANY, _('Filepath to music base file directory:'))
        labelSizer.Add(filePathLbl, 0, wx.ALL, 1)
        fileInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        labelSizer.Add(fileInputSizer, 1, wx.ALL | wx.EXPAND, 5)
        self.__fileInput = wx.TextCtrl(panel, wx.ID_ANY)

        if "musicDir" in properties:
            self.__fileInput.SetValue(properties["musicDir"])
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

        if "fileToken" in properties:
            self.__separatorInput.SetValue(properties["fileToken"])

        sepSizer.Add(self.__separatorInput, 0, wx.ALL | wx.EXPAND, 5)
        self.Bind(wx.EVT_TEXT, self.__onSeparatorTextChange, self.__separatorInput)

        #Separator description
        if "fileToken" in properties:
            self.__separatorDesc = wx.StaticText(panel, wx.ID_ANY, 
                                                 _('Filename structure with above separator: bpm' 
                                                   + properties["fileToken"] + 'category' 
                                                   + properties["fileToken"] + 'songtitle'
                                                   + properties["fileToken"] + 'artist.wav'))
        else:
            self.__separatorDesc = wx.StaticText(panel, wx.ID_ANY, _('Filename structure with above separator:'))

        labelSizer.Add(self.__separatorDesc, 0, wx.ALL, 5)

        #step change
        stepSizer = wx.BoxSizer(wx.HORIZONTAL)
        stepLbl = wx.StaticText(panel, wx.ID_ANY, 
                                _('Number of steps to add/substract when BPM is changed:'))
        stepSizer.Add(stepLbl, 1, wx.ALL | wx.EXPAND, 5)

        step = []
        for x in range(1, 21):
            step.append(str(x))

        for y in range(25, 101, 5):
            step.append(str(y))

        if "bpmStep" in properties:
            self.__stepCombo = wx.ComboBox(panel, wx.ID_ANY, style=wx.CB_READONLY, 
                                           value=properties["bpmStep"], choices=step)
        else:
            self.__stepCombo = wx.ComboBox(panel, wx.ID_ANY, style=wx.CB_READONLY,
                                           value="10", choices=step)

        stepSizer.Add(self.__stepCombo, 0, wx.ALL, 5)
        labelSizer.Add(stepSizer, 0, wx.ALL, 5)
        

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

        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

    def __onBrowse(self, event):
        """Browse button clicked."""

        fileDialog = wx.DirDialog(self, _('Choose music base file directory:'))
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return
                                
        self.__fileInput.SetValue(fileDialog.GetPath())

    def __onSeparatorTextChange(self, event):
        """Method is called when text in separator input is changed."""

        token = self.__separatorInput.GetValue()
        self.__separatorDesc.SetLabel(_('Filename structure with above separator: bpm' + token +
                                        'category' + token + 'songtitle' + token + 'atrist.wav'))
    
    def __onSave(self, event):
        """Save button clicked."""

        fPath = self.__fileInput.GetValue()

        if os.path.exists(fPath):
            filectrl.setProperty("musicDir", fPath)
            filectrl.setProperty("fileToken", self.__separatorInput.GetValue())
            filectrl.setProperty("bpmStep", self.__stepCombo.GetValue())
            self.GetParent().updateProperties()
            self.Destroy()
        else:
            error_msg = _("Directory does not exist: ") + fPath + _("\nPlease, specify an existing directory")
            dialog = wx.MessageDialog(self, error_msg, _("Directory does not exist"), 
                                      wx.OK | wx.ICON_ERROR)
            dialog.ShowModal()
            dialog.Destroy()

    def __onCancel(self, event):
       """Cancel button clicked."""
       self.Destroy()
