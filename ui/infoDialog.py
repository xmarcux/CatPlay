#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import threading
import datetime as dt

class InfoDialog(wx.Dialog):
    """
    This class is a dialog
    that shows the most important
    values in a big font to
    be able to see it from longer distance.
    """

    def __init__(self, *args, **kw):
        """Initialization"""

        self.__parent = args[0]
        self.__keyDownTime = 0
        super(InfoDialog, self).__init__(*args, **kw)
        self.SetTitle("Information")
        self.__createView()

    def __createView(self):
        """Method creates the view of the dialog."""
   
        panel = wx.Panel(self)
        panel.Bind(wx.EVT_KEY_DOWN, self.__onKeyDown)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        txtFont = wx.Font(30, wx.DECORATIVE, wx.NORMAL, wx.BOLD)

        self.__bpmLbl = wx.StaticText(panel, wx.ID_ANY, _('Current BPM: ') + '120')
        self.__bpmLbl.SetFont(txtFont)
        mainSizer.Add(self.__bpmLbl, 1, wx.CENTER)

        self.__timeLbl = wx.StaticText(panel, wx.ID_ANY, _('Time: ') + '01:34')
        self.__timeLbl.SetFont(txtFont)
        mainSizer.Add(self.__timeLbl, 1, wx.CENTER)

        mainSizer.Add(wx.StaticLine(panel, wx.ID_ANY), 0, wx.ALL | wx.EXPAND, 5)

        self.__infoLbl = wx.StaticText(panel, wx.ID_ANY, 'Information Information')
        self.__infoLbl.SetFont(txtFont)
        self.__infoLbl.SetForegroundColour((0, 0, 255))
        mainSizer.Add(self.__infoLbl, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(mainSizer)
        panel.SetFocus()
        mainSizer.Fit(self)
        self.__infoLbl.SetLabel('')

    def __onKeyDown(self, event):
        """Is called when a key is pressed."""

        if event.ControlDown():
            self.__keyDownTime = dt.datetime.now()
            key = event.GetKeyCode()
            if key == ord('P'):
                self.__infoLbl.SetLabel('Play')
                self.__parent._MainWindow__onPlay(self.__parent)
            elif key == ord('S'):
                self.__infoLbl.SetLabel('Stop')
                self.__parent._MainWindow__onStop(self.__parent)
            elif key == ord('B'):
                self.__infoLbl.SetLabel('Previous song')
                self.__parent._MainWindow__onPrevious(self.__parent)
            elif key == ord('N'):
                self.__infoLbl.SetLabel('Next song')
                self.__parent._MainWindow__onNext(self.__parent)
            elif key == ord('1'):
                self.__infoLbl.SetLabel('From BPM add')
                self.__parent._MainWindow__onFromBpmPlus(self.__parent)
            elif key == ord('2'):
                self.__infoLbl.SetLabel('From BPM substract')
                self.__parent._MainWindow__onFromBpmMinus(self.__parent)
            elif key == ord('3'):
                self.__infoLbl.SetLabel('To BPM add')
                self.__parent._MainWindow__onToBpmPlus(self.__parent)
            elif key == ord('4'):
                self.__infoLbl.SetLabel('To BPM substract')
                self.__parent._MainWindow__onToBpmMinus(self.__parent)
            elif key == ord('5'):
                self.__infoLbl.SetLabel('Added play time')
                self.__parent._MainWindow__onTimePlus(self.__parent)
            elif key == ord('6'):
                self.__infoLbl.SetLabel('Substraced play time')
                self.__parent._MainWindow__onTimeMinus(self.__parent)
            else:
                self.__clearInfoLbl()

            timer = threading.Timer(11, self.__clearInfoLbl)
            timer.start()

    def __clearInfoLbl(self):
        """Clears text in info label."""

        now = dt.datetime.now()
        diff = now - self.__keyDownTime

        if diff.total_seconds() > 10:
            self.__infoLbl.SetLabel('')

    def setTime(self, timeStr):
        """
        Updates time label.
        Time string format should be MM:SS
        """

        self.__timeLbl.SetLabel( _('Time: ') + timeStr)

    def setBPM(self, bpm):
        """Updates current BPM label."""

        self.__bpmLbl.SetLabel(_('Current BPM: ') + bpm)
