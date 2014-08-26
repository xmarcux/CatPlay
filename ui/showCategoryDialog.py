#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import wx
import filectrl
import autoSortListCtrl

class ShowCategoryDialog(wx.Frame):
    """
    Dialog that shows
    filepaths to music files 
    ordered in categories.
    """

    def __init__(self, parent, musicDict):
        """Initialization."""

        wx.Frame.__init__(self, parent)

        self.SetTitle(_('Show category files'))

        #Set window image
        image = wx.Image('db' + os.sep + 'img' + os.sep + 'catplay.png', 
                         wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(image)
        self.SetIcon(icon)

        self.__files = musicDict

        self.__createView()


    def __createView(self):
        """Method creates the view of the dialog"""

        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        #categories
        catSizer = wx.BoxSizer(wx.HORIZONTAL)
        catLbl = wx.StaticText(panel, wx.ID_ANY, _('Category:'))
        self.__categories = filectrl.getCategories()
        cat = self.__categories.values()
        cat.sort()

        if len(cat) > 0:
            self.__categoryCombo = wx.ComboBox(panel, wx.ID_ANY, style=wx.CB_READONLY,
                                               value=cat[0], choices=cat)
        else:
            self.__categoryCombo = wx.ComboBox(panel, wx.ID_ANY, style=wx.CB_READONLY)

        self.Bind(wx.EVT_TEXT, self.__categoryChanged, self.__categoryCombo)

        catSizer.Add(catLbl, 0, wx.ALL, 5)
        catSizer.Add(self.__categoryCombo, 0, wx.ALL, 5)
        mainSizer.Add(catSizer, 0, wx.ALL, 5)

        #token
        tokenSizer = wx.BoxSizer(wx.VERTICAL)

        charToken = ''  
        if len(self.__categories):
            for (k, v) in self.__categories.iteritems():
                if cat[0] == v:
                    charToken = k
                    break

        self.__tokenLbl = wx.StaticText(panel, wx.ID_ANY, 
                                        _('Character token for category: ') + charToken)
        tokenSizer.Add(self.__tokenLbl, wx.ALL, 5)
        mainSizer.Add(tokenSizer, 0, wx.ALL, 5)

        #music files list
        self.__filesList = autoSortListCtrl.AutoSortListCtrl(panel)
        mainSizer.Add(self.__filesList, 1, wx.ALL | wx.EXPAND, 5)
        if len(cat) > 0:
            self.__updateList(cat[0])

        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

    def __categoryChanged(self, event):
        """Method is called when category in combobox changes."""

        cat = self.__categoryCombo.GetValue()

        charToken = ''
        for (k, v) in self.__categories.iteritems():
            if cat == v:
                charToken = k
                break

        self.__tokenLbl.SetLabel(_('Character token for category: ') + charToken)
        self.__updateList(cat)


    def __updateList(self, category):
        """
        Updates music files list
        with files asociated with category.
        """

        self.__filesList.DeleteAllItems()

        for data in self.__files[category]:
            i = self.__filesList.InsertStringItem(sys.maxint, data)
