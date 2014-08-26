#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ColumnSorterMixin

"""A class that creates a table to show category music filepaths."""
class AutoSortListCtrl (wx.ListCtrl, ColumnSorterMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ColumnSorterMixin.__init__(self, 1)
        ListCtrlAutoWidthMixin.__init__(self)

        self.InsertColumn(0, _('Filepath'))

        self.itemDataMap = {}

    def GetListCtrl(self):
        return self
