#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os
import sys
import random
import threading
import time
import wx.media as m
import settingsDialog as sDialog
import categoryDialog as cDialog
import showCategoryDialog as showDialog
import filectrl as f

class MainWindow (wx.Frame):
    """Main window for application."""

    def __init__(self):
        """Init function."""

        wx.Frame.__init__(self, None, title=_('Cat Play'), size=(300, 300))
        self.__panel = wx.Panel(self, wx.ID_ANY)
#        self.Bind(wx.EVT_SIZE, self.__onResize)

        #Set window image
        image = wx.Image('db' + os.sep + 'img' + os.sep + 'catplay.png', 
                         wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(image)
        self.SetIcon(icon)

        #Get music files from directory
        self.__musicDict = f.getMusicFiles()
        #create play control

        if sys.platform == 'win32':
            self.__playCtrl = m.MediaCtrl(parent=self.__panel, szBackend=wx.media.MEDIABACKEND_WMP10)
        else:
            self.__playCtrl = m.MediaCtrl(parent=self.__panel)

        self.Bind(wx.media.EVT_MEDIA_LOADED, self.__songIsLoaded)
        self.Bind(wx.media.EVT_MEDIA_FINISHED, self.__playNext)
        self.__playCtrl.SetVolume(1.0)

        #Get properties from file
        self.__prop = f.getProperties()

        if "bpmStep" in self.__prop:
            self.__bpmStep = int(self.__prop["bpmStep"])
        else:
            self.__bpmStep = 10

        self.__fadeTime = 10

        self.CreateStatusBar()
        self.SetMenuBar(self.__createMenu())

        self.__createView()
        self.__setupKeybindings()
        self.__setupAboutInfo()

        self.Bind(wx.EVT_CLOSE, self.__onClose)

        self.__panel.SetSizerAndFit(self.__mainSizer)
        self.Fit()
        self.SetMinSize(self.GetEffectiveMinSize())
        self.Center()
        self.__panel.SetFocus()

        if not sys.platform == 'win32':
            self.__sizeRatioHeight = (self.GetSize().GetHeight()/self.__fromBpmLbl.GetFont().GetPointSize())
            self.__sizeRatioWidth = self.GetSize().GetWidth()/self.__fromBpmLbl.GetFont().GetPointSize()

        self.Show(True)

        if sys.platform == 'win32':
            self.__sizeRatioHeight = (self.GetSize().GetHeight()/self.__fromBpmLbl.GetFont().GetPointSize())
            self.__sizeRatioWidth = self.GetSize().GetWidth()/self.__fromBpmLbl.GetFont().GetPointSize()


    def __createMenu(self):
        """Method creates and initiates menu."""

        #File menu
        fileMenu = wx.Menu()
        fileExit = fileMenu.Append(wx.ID_EXIT, _('E&xit'), _('Terminate application'))
        self.Bind(wx.EVT_MENU, self.__onExit, fileExit)

        #Play menu
        playMenu = wx.Menu()
        playPrevious = playMenu.Append(wx.ID_BACKWARD, _('P&revious song'), _('Plays previous song in list'))
        self.Bind(wx.EVT_MENU, self.__onPrevious, playPrevious)
        playMenu.AppendSeparator()
        self.__menuPlayPlay = playMenu.Append(wx.ID_YES, _('&Play'), _('Plays current song'))
        self.Bind(wx.EVT_MENU, self.__onPlay, self.__menuPlayPlay)
        playStop = playMenu.Append(wx.ID_NO, _('&Stop'), _('Stops playing song'))
        self.Bind(wx.EVT_MENU, self.__onStop, playStop)
        playMenu.AppendSeparator()
        playNext = playMenu.Append(wx.ID_FORWARD, _('&Next song'), _('Plays next song in list'))
        self.Bind(wx.EVT_MENU, self.__onNext, playNext)

        #Category menu
        catMenu = wx.Menu()
        catShowCat = catMenu.Append(wx.ID_ANY, _('&Show categories...'), _('Show files in categories'))
        self.Bind(wx.EVT_MENU, self.__onShowCategory, catShowCat)
        catMenu.AppendSeparator()
        catAddCat = catMenu.Append(wx.ID_ADD, _('&Add category...'), _('Adds a category to library'))
        self.Bind(wx.EVT_MENU, self.__onAddCategory, catAddCat)
        catDelCat = catMenu.Append(wx.ID_REMOVE, _('&Delete category...'), _('Deletes category from library'))
        self.Bind(wx.EVT_MENU, self.__onDeleteCategory, catDelCat)


        #Tools menu
        toolsMenu = wx.Menu()
        settingsTools = toolsMenu.Append(wx.ID_PROPERTIES, _('&Settings...'),
                                           _('Change behaviour for application'))
        self.Bind(wx.EVT_MENU, self.__onSettings, settingsTools)

        #Help menu
        helpMenu = wx.Menu()
        aboutHelp = helpMenu.Append(wx.ID_ABOUT, _('&About CatPlay...'), 
                                    _('Information about application.'))
        self.Bind(wx.EVT_MENU, self.__onAbout, aboutHelp)

        #Create menubar
        menubar = wx.MenuBar()
        menubar.Append(fileMenu, _('&File'))
        menubar.Append(playMenu, _('&Play'))
        menubar.Append(catMenu, _('&Category'))
        menubar.Append(toolsMenu, _('&Tools'))
        menubar.Append(helpMenu, _('&Help'))

        return menubar

    def __createView(self):
        """Creates the view in the main window."""

        self.__mainSizer = wx.BoxSizer(wx.VERTICAL)

        #Play buttons
        playBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        bpmPrevious = wx.Image("db" + os.sep + "img" + os.sep + "previous.png", 
                               wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        bpmPreviousPressed = wx.Image("db" + os.sep + "img" + os.sep + "previous_pressed.png",
                                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        btnPrevious = wx.BitmapButton(self.__panel, wx.ID_ANY, bpmPrevious)
        btnPrevious.SetBitmapSelected(bpmPreviousPressed)
        self.Bind(wx.EVT_BUTTON, self.__onPrevious, btnPrevious)
        playBtnSizer.Add(btnPrevious, 0, wx.ALL, 5)

        self.__bpmPlay = wx.Image("db" + os.sep + "img" + os.sep + "play.png", 
                           wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.__bpmPlayPressed = wx.Image("db" + os.sep + "img" + os.sep + "play_pressed.png",
                                         wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.__btnPlay = wx.BitmapButton(self.__panel, wx.ID_ANY, self.__bpmPlay)
        self.__btnPlay.SetBitmapSelected(self.__bpmPlayPressed)
        self.__bpmPause = wx.Image("db" + os.sep + "img" + os.sep + "pause.png",
                                   wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.__bpmPausePressed = wx.Image("db" + os.sep + "img" + os.sep + "pause_pressed.png",
                                          wx.BITMAP_TYPE_PNG).ConvertToBitmap()

        self.__btnPlay.play = "stop"
        self.Bind(wx.EVT_BUTTON, self.__onPlay, self.__btnPlay)
        playBtnSizer.Add(self.__btnPlay, 0, wx.ALL, 5)

        bpmStop = wx.Image("db" + os.sep + "img" + os.sep + "stop.png", 
                           wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        bpmStopPressed = wx.Image("db" + os.sep + "img" + os.sep + "stop_pressed.png", 
                                  wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        btnStop = wx.BitmapButton(self.__panel, wx.ID_ANY, bpmStop)
        btnStop.SetBitmapSelected(bpmStopPressed)
        self.Bind(wx.EVT_BUTTON, self.__onStop, btnStop)
        playBtnSizer.Add(btnStop, 0, wx.ALL, 5)

        bpmNext = wx.Image("db" + os.sep + "img" + os.sep + "next.png", 
                           wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        bpmNextPressed = wx.Image("db" + os.sep + "img" + os.sep + "next_pressed.png", 
                                  wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.__btnNext = wx.BitmapButton(self.__panel, wx.ID_ANY, bpmNext)
        self.__btnNext.SetBitmapSelected(bpmNextPressed)
        self.Bind(wx.EVT_BUTTON, self.__onNext, self.__btnNext)
        playBtnSizer.Add(self.__btnNext, 0, wx.ALL, 5)
        self.__mainSizer.Add(playBtnSizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        #Info current song
        txtFont = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        infoBox = wx.StaticBox(self.__panel, wx.ID_ANY, _('Current song playing:'))
        infoSizer = wx.StaticBoxSizer(infoBox, wx.HORIZONTAL)
        artistLbl = wx.StaticText(self.__panel, wx.ID_ANY, _('Artist:'))
        artistLbl.SetFont(txtFont)
        self.__currentArtistLbl = wx.StaticText(self.__panel, wx.ID_ANY, _(''))
        self.__currentArtistLbl.SetFont(txtFont)
        songLbl = wx.StaticText(self.__panel, wx.ID_ANY, _('Title:'))
        songLbl.SetFont(txtFont)
        self.__currentTitleLbl = wx.StaticText(self.__panel, wx.ID_ANY, _(''))
        self.__currentTitleLbl.SetFont(txtFont)
        infoSizer.Add(artistLbl, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        infoSizer.Add(self.__currentArtistLbl, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        infoSizer.Add(songLbl, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        infoSizer.Add(self.__currentTitleLbl, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        self.__mainSizer.Add(infoSizer, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        #from BPM control
        bpmSizer = wx.BoxSizer(wx.HORIZONTAL)
        fromBpmBox = wx.StaticBox(self.__panel, wx.ID_ANY, _('From BPM:'))
        self.__fromBpmSizer = wx.StaticBoxSizer(fromBpmBox, wx.VERTICAL)
        self.__fromBpm = "140"
        if "fromBpm" in self.__prop:
            self.__fromBpmLbl = wx.StaticText(self.__panel, wx.ID_ANY, self.__prop["fromBpm"])
            self.__fromBpm = self.__prop["fromBpm"]
        else:
            self.__fromBpmLbl = wx.StaticText(self.__panel, wx.ID_ANY, "140")
        bpmFont = wx.Font(80, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.__fromBpmLbl.SetFont(bpmFont)
        self.__fromBpmSizer.Add(self.__fromBpmLbl, 1, wx.ALL, 5)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__bpmPlus = wx.Image("db" + os.sep + "img" + os.sep + "plus.png",
                                  wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.__bpmPlusPressed = wx.Image("db" +os.sep + "img" + os.sep + "plus_pressed.png",
                                         wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.__fromAddBtn = wx.BitmapButton(self.__panel, wx.ID_ANY, self.__bpmPlus)
        self.__fromAddBtn.SetBitmapSelected(self.__bpmPlusPressed)
        self.Bind(wx.EVT_BUTTON, self.__onFromBpmPlus, self.__fromAddBtn)
        self.__bpmMinus = wx.Image("db" + os.sep + "img" + os.sep + "minus.png",
                                   wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.__bpmMinusPressed = wx.Image("db" + os.sep + "img" + os.sep + "minus_pressed.png",
                                          wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.__fromSubBtn = wx.BitmapButton(self.__panel, wx.ID_ANY, self.__bpmMinus)
        self.__fromSubBtn.SetBitmapSelected(self.__bpmMinusPressed)
        self.Bind(wx.EVT_BUTTON, self.__onFromBpmMinus, self.__fromSubBtn)
        btnSizer.Add(self.__fromAddBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.__fromSubBtn, 0, wx.ALL, 5)
        self.__fromBpmSizer.Add(btnSizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        bpmSizer.Add(self.__fromBpmSizer, 0, wx.ALL, 5)

        #to BPM control
        toBpmBox = wx.StaticBox(self.__panel, wx.ID_ANY, _('To BPM:'))
        toBpmSizer = wx.StaticBoxSizer(toBpmBox, wx.VERTICAL)
        self.__toBpm = "160"
        if "toBpm" in self.__prop:
            self.__toBpmLbl = wx.StaticText(self.__panel, wx.ID_ANY, self.__prop["toBpm"])
            self.__toBpm = self.__prop["toBpm"]
        else: 
            self.__toBpmLbl = wx.StaticText(self.__panel, wx.ID_ANY, "160")
        self.__toBpmLbl.SetFont(bpmFont)
        toBpmSizer.Add(self.__toBpmLbl, 1, wx.ALL | wx.ALIGN_CENTER, 5)
        toBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__toAddBtn = wx.BitmapButton(self.__panel, wx.ID_ANY, self.__bpmPlus)
        self.__toAddBtn.SetBitmapSelected(self.__bpmPlusPressed)
        self.Bind(wx.EVT_BUTTON, self.__onToBpmPlus, self.__toAddBtn)
        self.__toSubBtn = wx.BitmapButton(self.__panel, wx.ID_ANY, self.__bpmMinus)
        self.__toSubBtn.SetBitmapSelected(self.__bpmMinusPressed)
        self.Bind(wx.EVT_BUTTON, self.__onToBpmMinus, self.__toSubBtn)
        toBtnSizer.Add(self.__toAddBtn, 0, wx.ALL, 5)
        toBtnSizer.Add(self.__toSubBtn, 0, wx.ALL, 5)
        toBpmSizer.Add(toBtnSizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        bpmSizer.Add(toBpmSizer, 0, wx.ALL, 5)

        self.__mainSizer.Add(bpmSizer, 1, wx.ALL | wx.ALIGN_CENTER, 5)

        #Category
        self.__categorySizer = wx.BoxSizer(wx.HORIZONTAL)
        categoryLbl = wx.StaticText(self.__panel, wx.ID_ANY, _('Category:'))
        categoryLbl.SetFont(txtFont)
        self.__categorySizer.Add(categoryLbl, 0, wx.ALL, 5)
        #get categories from file
        coi = f.getCategories().values()
        coi.sort()
        self.__category = ""

        if len(coi):
            index = 0
            if "category" in self.__prop:
                if (self.__prop["category"] in coi) and (len(coi) > 0):
                    index = coi.index(self.__prop["category"])
                self.__category = coi[index]
            if sys.platform == 'win32':
                self.__categoryCombo = wx.ComboBox(self.__panel, wx.ID_ANY, style=wx.CB_READONLY, 
                                                   value=coi[index], choices=coi)
            else:
                self.__categoryCombo = wx.Choice(self.__panel, wx.ID_ANY, style=wx.CB_READONLY, 
                                                 choices=coi)
        else:
            if sys.platform == 'win32':
                self.__categoryCombo = wx.ComboBox(self.__panel, wx.ID_ANY, style=wx.CB_READONLY, 
                                                   choices=coi)
            else: 
                self.__categoryCombo = wx.Choice(self.__panel, wx.ID_ANY, style=wx.CB_READONLY, 
                                                 choices=coi)
        self.__categoryCombo.SetFont(txtFont)
        self.__categorySizer.Add(self.__categoryCombo, 0, wx.ALL, 5)
        self.__mainSizer.Add(self.__categorySizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        #Song time
        timeBox = wx.StaticBox(self.__panel, wx.ID_ANY, _('Time between song changes:'))
        timeBoxSizer = wx.StaticBoxSizer(timeBox, wx.VERTICAL)
        self.__time = "02:30"
        if "time" in self.__prop:
            self.__timeCheckBox = wx.CheckBox(self.__panel, wx.ID_ANY, self.__prop["time"])
            self.__time = self.__prop["time"]
        else:
            self.__timeCheckBox = wx.CheckBox(self.__panel, wx.ID_ANY, "02:30")
        timeFont = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.__timeCheckBox.SetFont(timeFont)
        self.__timeCheckBox.SetToolTip(wx.ToolTip(
                                       _('Enable/disable time between song changes, if disabled full songs will be played.')))
        timeBoxSizer.Add(self.__timeCheckBox, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        timeBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__timeAddBtn = wx.BitmapButton(self.__panel, wx.ID_ANY, self.__bpmPlus)
        self.__timeAddBtn.SetBitmapSelected(self.__bpmPlusPressed)
        self.Bind(wx.EVT_BUTTON, self.__onTimePlus, self.__timeAddBtn)
        self.__timeSubBtn = wx.BitmapButton(self.__panel, wx.ID_ANY, self.__bpmMinus)
        self.__timeSubBtn.SetBitmapSelected(self.__bpmMinusPressed)
        self.Bind(wx.EVT_BUTTON, self.__onTimeMinus, self.__timeSubBtn)
        timeBtnSizer.Add(self.__timeAddBtn, 0, wx.ALL, 5)
        timeBtnSizer.Add(self.__timeSubBtn, 0, wx.ALL, 5)
        timeBoxSizer.Add(timeBtnSizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.__mainSizer.Add(timeBoxSizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.__panel.SetSizer(self.__mainSizer)
        self.__mainSizer.Fit(self)

    def __setupKeybindings(self):
        """
        Setup the key bindings 
        for buttons in main window.
        """

        keyPlay = wx.NewId()
        wx.EVT_MENU(self, keyPlay, self.__onPlay)
        keyStop = wx.NewId()
        wx.EVT_MENU(self, keyStop, self.__onStop)
        keyPrevious = wx.NewId()
        wx.EVT_MENU(self, keyPrevious, self.__onPrevious)
        keyNext = wx.NewId()
        wx.EVT_MENU(self, keyNext, self.__onNext)

        keyFromBpmPlus = wx.NewId()
        wx.EVT_MENU(self, keyFromBpmPlus, self.__onFromBpmPlus)
        keyFromBpmMinus = wx.NewId()
        wx.EVT_MENU(self, keyFromBpmMinus, self.__onFromBpmMinus)

        keyToBpmPlus = wx.NewId()
        wx.EVT_MENU(self, keyToBpmPlus, self.__onToBpmPlus)
        keyToBpmMinus = wx.NewId()
        wx.EVT_MENU(self, keyToBpmMinus, self.__onToBpmMinus)

        keyTimePlus = wx.NewId()
        wx.EVT_MENU(self, keyTimePlus, self.__onTimePlus)
        keyTimeMinus = wx.NewId()
        wx.EVT_MENU(self, keyTimeMinus, self.__onTimeMinus)

        acc_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('P'), keyPlay),
                                       (wx.ACCEL_CTRL, ord('S'), keyStop),
                                       (wx.ACCEL_CTRL, ord('B'), keyPrevious),
                                       (wx.ACCEL_CTRL, ord('N'), keyNext),
                                       (wx.ACCEL_CTRL, ord('1'), keyFromBpmPlus),
                                       (wx.ACCEL_CTRL, ord('2'), keyFromBpmMinus),
                                       (wx.ACCEL_CTRL, ord('3'), keyToBpmPlus),
                                       (wx.ACCEL_CTRL, ord('4'), keyToBpmMinus),
                                       (wx.ACCEL_CTRL, ord('5'), keyTimePlus),
                                       (wx.ACCEL_CTRL, ord('6'), keyTimeMinus)
                                     ])
        self.SetAcceleratorTable(acc_tbl)

    def __setupAboutInfo(self):
        """Initialize the about info dialog."""

        self.__aboutInfo = wx.AboutDialogInfo()
        self.__aboutInfo.SetName('CatPlay')
        self.__aboutInfo.SetVersion('V0.9.0')
        self.__aboutInfo.SetDevelopers(['Marcus Pedersén'])
        self.__aboutInfo.SetCopyright('CatPlay (C) 2014 Marcus Pedersén')
        self.__aboutInfo.SetDescription(_('Play your categorized songs.'))
        self.__aboutInfo.SetLicense('This program is free software: you can redistribute it and/or modify\n'
                                  'it under the terms of the GNU General Public License as published by\n'
                                  'the Free Software Foundation, either version 3 of the License, or\n'
                                  '(at your option) any later version.\n'
                                  '\n'
                                  'This program is distributed in the hope that it will be useful,\n'
                                  'but WITHOUT ANY WARRANTY; without even the implied warranty of\n'
                                  'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n'
                                  'GNU General Public License for more details.\n'
                                  '\n'
                                  'You should have received a copy of the GNU General Public License\n'
                                  'along with this program. If not, see http://www.gnu.org/licenses/\n'
                                  '\n' 
                                  'Contact: marcux@marcux.org\n'
                                  'Repro: https://github.com/xmarcux/catplay\n')


    def updateCategories(self):
        """
        Get current categories 
        from file and update combo.
        Used when category is added
        or deleted.
        """

        cat = f.getCategories().values()
        cat.sort()
        if len(cat):
            self.__categoryCombo.SetItems(cat)
            self.__categoryCombo.SetSelection(0)
        else:
            self.__categoryCombo.Clear()
            self.__categoryCombo.SetValue("")


    def updateProperties(self):
        """
        Get current properties
        from file and update variables
        in this instance.
        """

        prop = f.getProperties()
        if "bpmStep" in prop:
            self.__bpmStep = int(prop["bpmStep"])

    def __onExit(self, event):
        """Terminates application"""
        self.Close()

    def __onShowCategory(self, event):
        """Show category information dialog"""

        self.__musicDict = f.getMusicFiles()

        dialog = showDialog.ShowCategoryDialog(self, self.__musicDict)
        dialog.Center()
        dialog.Show()

    def __onAddCategory(self, event):
        """Add a category to library"""

        dialog = cDialog.AddCategoryDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def __onDeleteCategory(self, event):
        """Removes category from library"""

        dialog = cDialog.DeleteCategoryDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def __onPrevious(self, event):
        """Previous song button has been clicked."""

        if self.__btnPlay.play == "play" or self.__btnPlay.play == "pause":
            self.__reloadPlaylistIfChanged()
            if self.__currentSongNumber <= 0:
                self.__currentSongNumber = len(self.__playList) - 1
            else:
                self.__currentSongNumber -= 1
 
            self.__loadFile()
        
            if self.__timeCheckBox.GetValue():
                self.__timer.cancel()

            if self.__btnPlay.play == "play":
                self.__startTimer()

    def __onNext(self, event):
        """Next song button has been clicked."""

        if self.__btnPlay.play == "play" or self.__btnPlay.play == "pause":
            self.__reloadPlaylistIfChanged()
            if self.__currentSongNumber >= len(self.__playList) + 1:
                self.__currentSongNumber = 0
            else:
                self.__currentSongNumber += 1

            self.__loadFile()

            if self.__timeCheckBox.GetValue():
                self.__timer.cancel()

            if self.__btnPlay.play == "play":
                self.__startTimer()


    def __onPlay(self, event):
        """Play button has been clicked."""

        if self.__btnPlay.play == "play":
            self.__btnPlay.SetBitmapLabel(self.__bpmPlay)
            self.__btnPlay.SetBitmapSelected(self.__bpmPlayPressed)
            self.__menuPlayPlay.SetText(_('Play'))
            self.SetStatusText(_('Pause'))
            self.__btnPlay.play = "pause"
            self.__playCtrl.Pause()
            
            if self.__timeCheckBox.GetValue():
                self.__timer.cancel()

        else:
            self.__createPlayList()
            if self.__btnPlay.play == "stop":
                self.__loadFile()

            if self.__btnPlay.play == "pause":
                self.__playCtrl.Play()

            self.__btnPlay.SetBitmapLabel(self.__bpmPause)
            self.__btnPlay.SetBitmapSelected(self.__bpmPausePressed)
            self.__menuPlayPlay.SetText(_('Pause'))
            self.SetStatusText(_('Play'))
            self.__btnPlay.play = "play"
            self.__startTimer()

    def __onStop(self, event):
        """Stop to play button has been clicked."""

        self.SetStatusText(_('Stop'))

        self.__btnPlay.SetBitmapLabel(self.__bpmPlay)
        self.__btnPlay.SetBitmapSelected(self.__bpmPlayPressed)
        self.__menuPlayPlay.SetText(_('Play'))
        self.__btnPlay.play = "stop"
        self.__fromAddBtn.Enable()
        self.__fromSubBtn.Enable()
        self.__toAddBtn.Enable()
        self.__toSubBtn.Enable()
        self.__timeCheckBox.Enable()
        self.__timeAddBtn.Enable()
        self.__timeSubBtn.Enable()
        self.__categoryCombo.Enable()
        self.__playCtrl.Stop()

        try:
            self.__timer.cancel()
        except:
            pass


    def __onSettings(self, event):
        """"Menu tools, settings is clicked."""

        dialog = sDialog.SettingsDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def __onAbout(self, event):
        """Menu help, about is clicked."""

        wx.AboutBox(self.__aboutInfo)

    def __onFromBpmPlus(self, event):
        """Plus button from BPM is clicked."""

        newValue = int(self.__fromBpmLbl.GetLabel()) + self.__bpmStep
        if newValue > int(self.__toBpmLbl.GetLabel()):
            newValue = int(self.__toBpmLbl.GetLabel())

        if newValue < 100:
            newValue = '  ' + str(newValue)
        if newValue < 10:
            newValue = '  ' + str(newValue)

        self.__fromBpmLbl.SetLabel(str(newValue))

    def __onFromBpmMinus(self, event):
        """Minus button from BPM is clicked."""

        newValue = int(self.__fromBpmLbl.GetLabel()) - self.__bpmStep
        if newValue < 0:
            newValue = 0

        if newValue < 100:
            newValue = '  ' + str(newValue)
        if newValue < 10:
            newValue = '  ' + str(newValue)

        self.__fromBpmLbl.SetLabel(str(newValue))

    def __onToBpmPlus(self, event):
        """Plus button to BPM is clicked."""
  
        newValue = int(self.__toBpmLbl.GetLabel()) + self.__bpmStep
        if newValue > 500:
            newValue = 500

        if newValue < 100:
            newValue = '  ' + str(newValue)
        if newValue < 10:
            newValue = '  ' + str(newValue)

        self.__toBpmLbl.SetLabel(str(newValue))

    def __onToBpmMinus(self, event):
        """Minus button to BPM is clicked."""

        newValue = int(self.__toBpmLbl.GetLabel()) - self.__bpmStep
        if newValue < int(self.__fromBpmLbl.GetLabel()):
            newValue = int(self.__fromBpmLbl.GetLabel())

        if newValue < 100:
            newValue = '  ' + str(newValue)
        if newValue < 10:
            newValue = '  ' + str(newValue)

        self.__toBpmLbl.SetLabel(str(newValue))

    def __onTimePlus(self, event):
        """Plus button on song time clicked."""

        min = int(self.__timeCheckBox.GetLabel().split(':')[0])
        sec = int(self.__timeCheckBox.GetLabel().split(':')[1])
        if min < 20:
            if sec >= 55:
                sec = 0
                min += 1
            else:
                sec += 5

            sMin = str(min)
            sSec = str(sec)
            if min < 10:
                sMin = '0' + sMin
            if sec < 10:
                sSec = '0' + sSec

            self.__timeCheckBox.SetLabel(sMin + ':' + sSec)

    def __onTimeMinus(self, event):
        """Minus button on song time clicked."""

        min = int(self.__timeCheckBox.GetLabel().split(':')[0])
        sec = int(self.__timeCheckBox.GetLabel().split(':')[1])
        if not (min == 0 and sec == 0):
            if sec == 0:
                sec = 55
                min -= 1
            else:
                if not (min == 0 and sec <= 20):
                    sec -= 5

            sMin = str(min)
            sSec = str(sec)
            if min < 10:
                sMin = '0' + sMin
            if sec < 10:
                sSec = '0' + sSec

            self.__timeCheckBox.SetLabel(sMin + ':' + sSec)

    def __onClose(self, event):
        """Is called when window is closing."""
        f.setProperty("fromBpm", self.__fromBpmLbl.GetLabel())
        f.setProperty("toBpm", self.__toBpmLbl.GetLabel())
        f.setProperty("time", self.__timeCheckBox.GetLabel())
        if sys.platform == 'win32':
            f.setProperty("category", self.__categoryCombo.GetValue())

        try:
            self.__playCtrl.Stop()
            self.__timer.cancel()
        except:
            pass

        self.Destroy()

    def __onResize(self, event):

        self.SetSize(event.GetSize())
        lblRatio = int(((event.GetSize().GetHeight()+event.GetSize().GetWidth())/2)
                       /((self.__sizeRatioHeight+self.__sizeRatioWidth)/2))

        bpmYBottom = self.__fromBpmSizer.GetPosition().Get()[1] +  self.__fromBpmSizer.GetSize().GetHeight()
        catYTop = self.__categorySizer.GetPosition().Get()[1]
        fnt = self.__fromBpmLbl.GetFont()

        if (bpmYBottom < catYTop) or (lblRatio < fnt.GetPointSize()):
            fnt.SetPointSize(lblRatio)
            self.__fromBpmLbl.SetFont(fnt)
            self.__toBpmLbl.SetFont(fnt)

        event.Skip()

    def __createPlayList(self):
        """
        Method creates the current
        playlist based on max and 
        min bpm plus current category.
        """

        self.__playList = []

        self.__musicDict = f.getMusicFiles()

        if sys.platform == 'win32':
            tmpList = self.__musicDict[self.__categoryCombo.GetValue()]
        else:
            itm = self.__categoryCombo.GetItems()
            tmpList = self.__musicDict[itm[self.__categoryCombo.GetSelection()]]

        tmpList.sort()
        minBpm = int(self.__fromBpmLbl.GetLabel())
        maxBpm = int(self.__toBpmLbl.GetLabel())
        token = self.__prop["fileToken"]

        for m in tmpList:
            fileName = m.split(os.sep)
            fileName = fileName[len(fileName)-1]
            splitStr = fileName.split(token)
            bpm = int(splitStr[0])
            if bpm >= minBpm and bpm <= maxBpm:
                self.__playList.append(m)
        
        random.shuffle(self.__playList)
        self.__currentSongNumber = 0

    def __loadFile(self):
        """
        Loads the next song to play
        in ui and in media control.
        """

        if len(self.__playList) <= self.__currentSongNumber or self.__currentSongNumber < 0:
            self.__currentSongNumber = 0

        if len(self.__playList) > 0 and len(self.__playList) > self.__currentSongNumber:
            token = self.__prop["fileToken"]
            fileName = self.__playList[self.__currentSongNumber].split(os.sep)
            fileName = fileName[len(fileName)-1].split('.')[0]
            fileName = fileName.split(token)
            if len(fileName) >= 4:
                self.__currentArtistLbl.SetLabel(fileName[2])
                self.__currentTitleLbl.SetLabel(fileName[3])
                self.__playCtrl.Stop()
                self.__playCtrl.Load(self.__playList[self.__currentSongNumber])


    def __songIsLoaded(self, evt):
        """
        Function is called when song
        is loaded. Bound to media ctrl.
        """
        if self.__btnPlay.play != "pause":
            self.__playCtrl.Play()

    def __playNext(self, evt):
        """
        Function is called when song
        has finished playing.
        """
        self.__reloadPlaylistIfChanged()
        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.__btnNext.GetId())
        wx.PostEvent(self.__btnNext, evt)
        

    def __startTimer(self):
        """
        Starts timer that changes song
        after set time.
        """

        min = int(self.__timeCheckBox.GetLabel().split(':')[0])
        sec = int(self.__timeCheckBox.GetLabel().split(':')[1])
        sec = int(sec) + int(min) * 60
        sec = sec - self.__fadeTime
        
        self.__timer = threading.Timer(sec, self.__fadeChangeSong)

        if self.__timeCheckBox.GetValue():
            self.__timer.start()

    def __fadeChangeSong(self):
        """
        Fades the current song out,
        changes song and fades the
        new song in.
        """

        vol = 1.0
        decrease = 1.0/(self.__fadeTime * 2)

        while vol > 0.0:
            self.__playCtrl.SetVolume(vol)
            time.sleep(0.5)
            vol -= decrease

        self.__playCtrl.Stop()
        self.__playCtrl.SetVolume(1.0)

        time.sleep(1.0)

        """
        Check if bpm, category or time has change.
        If they have update variables and reload playlist.
        """
        self.__reloadPlaylistIfChanged()

        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.__btnNext.GetId())
        wx.PostEvent(self.__btnNext, evt)

        vol = 0.0
        while vol < 1.0:
            vol += decrease
            self.__playCtrl.SetVolume(vol)
            time.sleep(0.5)

    def __reloadPlaylistIfChanged(self):
        """
        Checks if bpm, category or/and time
        has changed since last time.
        If any of them have changed,
        variables are updated and 
        new playlist is loaded.
        """

        changed = False
        toBpm = self.__toBpmLbl.GetLabel()
        fromBpm = self.__fromBpmLbl.GetLabel()
        time = self.__timeCheckBox.GetLabel()

        if sys.platform == 'win32':
            category = self.__categoryCombo.GetValue()
        else:
            category = self.__categoryCombo.GetLabelText()


        if toBpm != self.__toBpm:
            self.__toBpm = toBpm
            changed = True

        if fromBpm != self.__fromBpm:
            self.__fromBpm = fromBpm
            changed = True

        if category != self.__category:
            self.__category = category
            changed = True

        if time != self.__time:
            self.__time = time
            changed = True

        self.__createPlayList()
