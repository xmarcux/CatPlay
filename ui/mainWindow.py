#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import settingsDialog as sDialog
import categoryDialog as cDialog

class MainWindow (wx.Frame):
    """Main window for application."""

    def __init__(self):
        """Init function."""

        wx.Frame.__init__(self, None, title=_('Cat Play'), size=(300, 300))
        self.__panel = wx.Panel(self, wx.ID_ANY)

        self.CreateStatusBar()
        self.SetMenuBar(self.__createMenu())

        self.__panel = wx.Panel(self, wx.ID_ANY)
        self.__createView()

        self.__setupAboutInfo()

        self.__panel.SetSizerAndFit(self.__mainSizer)
        self.Fit()
        self.SetMinSize(self.GetEffectiveMinSize())
        self.Center()
        self.Show(True)


    def __createMenu(self):
        """Method creates and initiates menu."""

        #File menu
        fileMenu = wx.Menu()
        fileAddCat = fileMenu.Append(wx.ID_ADD, _('&Add category...'), _('Adds a category to library'))
        self.Bind(wx.EVT_MENU, self.__onAddCategory, fileAddCat)
        fileDelCat = fileMenu.Append(wx.ID_REMOVE, _('&Delete category...'), _('Deletes category from library'))
        self.Bind(wx.EVT_MENU, self.__onDeleteCategory, fileDelCat)
        fileMenu.AppendSeparator()
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
        menubar.Append(toolsMenu, _('&Tools'))
        menubar.Append(helpMenu, _('&Help'))

        return menubar

    def __createView(self):
        """Creates the view in the main window."""

        self.__mainSizer = wx.BoxSizer(wx.VERTICAL)
        #topSizer = wx.BoxSizer(wx.VERTICAL)
        #self.__mainSizer.Add(topSizer, 1, wx.ALL | wx.EXPAND, 5)
        
        #Play buttons
        playBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnPrevious = wx.Button(self.__panel, wx.ID_ANY, _('Previous'))
        self.Bind(wx.EVT_BUTTON, self.__onPrevious, btnPrevious)
        playBtnSizer.Add(btnPrevious, 0, wx.ALL, 5)
        self.__btnPlay = wx.Button(self.__panel, wx.ID_ANY, _('Play'))
        self.__btnPlay.play = "pause"
        self.Bind(wx.EVT_BUTTON, self.__onPlay, self.__btnPlay)
        playBtnSizer.Add(self.__btnPlay, 0, wx.ALL, 5)
        btnStop = wx.Button(self.__panel, wx.ID_ANY, _('Stop'))
        self.Bind(wx.EVT_BUTTON, self.__onStop, btnStop)
        playBtnSizer.Add(btnStop, 0, wx.ALL, 5)
        btnNext = wx.Button(self.__panel, wx.ID_ANY, _('Next'))
        self.Bind(wx.EVT_BUTTON, self.__onNext, btnNext)
        playBtnSizer.Add(btnNext, 0, wx.ALL, 5)
        self.__mainSizer.Add(playBtnSizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        #Info current song
        infoBox = wx.StaticBox(self.__panel, wx.ID_ANY, _('Current song playing:'))
        infoSizer = wx.StaticBoxSizer(infoBox, wx.HORIZONTAL)
        artistLbl = wx.StaticText(self.__panel, wx.ID_ANY, _('Artist:'))
        self.__currentArtistLbl = wx.StaticText(self.__panel, wx.ID_ANY, _('De lyckliga kompisarna'))
        songLbl = wx.StaticText(self.__panel, wx.ID_ANY, _('Title:'))
        self.__currentTitleLbl = wx.StaticText(self.__panel, wx.ID_ANY, _('Finansministern'))
        infoSizer.Add(artistLbl, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        infoSizer.Add(self.__currentArtistLbl, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        infoSizer.Add(songLbl, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        infoSizer.Add(self.__currentTitleLbl, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        self.__mainSizer.Add(infoSizer, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        #from BPM control
        bpmSizer = wx.BoxSizer(wx.HORIZONTAL)
        fromBpmBox = wx.StaticBox(self.__panel, wx.ID_ANY, _('From BPM:'))
        fromBpmSizer = wx.StaticBoxSizer(fromBpmBox, wx.VERTICAL)
        self.__fromBpmLbl = wx.StaticText(self.__panel, wx.ID_ANY, "140")
        bpmFont = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.__fromBpmLbl.SetFont(bpmFont)
        fromBpmSizer.Add(self.__fromBpmLbl, 1, wx.ALL | wx.ALIGN_CENTER, 5)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        fromAddBtn = wx.Button(self.__panel, wx.ID_ANY, "+")
        fromSubBtn = wx.Button(self.__panel, wx.ID_ANY, "-")
        btnSizer.Add(fromAddBtn, 0, wx.ALL, 5)
        btnSizer.Add(fromSubBtn, 0, wx.ALL, 5)
        fromBpmSizer.Add(btnSizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        bpmSizer.Add(fromBpmSizer, 0, wx.ALL, 5)

        #to BPM control
        toBpmBox = wx.StaticBox(self.__panel, wx.ID_ANY, _('To BPM:'))
        toBpmSizer = wx.StaticBoxSizer(toBpmBox, wx.VERTICAL)
        self.__toBpmLbl = wx.StaticText(self.__panel, wx.ID_ANY, "160")
        self.__toBpmLbl.SetFont(bpmFont)
        toBpmSizer.Add(self.__toBpmLbl, 1, wx.ALL | wx.ALIGN_CENTER, 5)
        toBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        toAddBtn = wx.Button(self.__panel, wx.ID_ANY, "+")
        toSubBtn = wx.Button(self.__panel, wx.ID_ANY, "-")
        toBtnSizer.Add(toAddBtn, 0, wx.ALL, 5)
        toBtnSizer.Add(toSubBtn, 0, wx.ALL, 5)
        toBpmSizer.Add(toBtnSizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        bpmSizer.Add(toBpmSizer, 0, wx.ALL, 5)
        self.__mainSizer.Add(bpmSizer, 0, wx.ALL | wx.EXPAND, 5)

        #Category
        categorySizer = wx.BoxSizer(wx.HORIZONTAL)
        categoryLbl = wx.StaticText(self.__panel, wx.ID_ANY, _('Category:'))
        categorySizer.Add(categoryLbl, 0, wx.ALL, 5)
        #test
        coi = ['Bugg', 'Jazz', 'Foxstrot', 'Vals']
        #test end
        self.__categoryCombo = wx.ComboBox(self.__panel, wx.ID_ANY, style=wx.CB_READONLY, 
                                           value=coi[0], choices=coi)
        categorySizer.Add(self.__categoryCombo, 0, wx.ALL, 5)
        self.__mainSizer.Add(categorySizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        #Song time
        timeBox = wx.StaticBox(self.__panel, wx.ID_ANY, _('Time between song changes:'))
        timeBoxSizer = wx.StaticBoxSizer(timeBox, wx.VERTICAL)
        self.__timeCheckBox = wx.CheckBox(self.__panel, wx.ID_ANY, "02:30")
        timeFont = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.__timeCheckBox.SetFont(timeFont)
        self.__timeCheckBox.SetToolTip(wx.ToolTip(
                                       _('Anable/disable time between song changes, if disabled full songs will be played.')))
        timeBoxSizer.Add(self.__timeCheckBox, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        timeBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        timeAddBtn = wx.Button(self.__panel, wx.ID_ANY, "+")
        timeSubBtn = wx.Button(self.__panel, wx.ID_ANY, "-")
        timeBtnSizer.Add(timeAddBtn, 0, wx.ALL, 5)
        timeBtnSizer.Add(timeSubBtn, 0, wx.ALL, 5)
        timeBoxSizer.Add(timeBtnSizer, 0, wx.ALL, 5)
        self.__mainSizer.Add(timeBoxSizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.__panel.SetSizer(self.__mainSizer)
        self.__mainSizer.Fit(self)

    def __setupAboutInfo(self):
        """Initialize the about info dialog."""

        self.__aboutInfo = wx.AboutDialogInfo()
        self.__aboutInfo.SetName('CatPlay')
        self.__aboutInfo.SetVersion('1.0.0')
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


    def __onExit(self, event):
        """Terminates application"""

        self.Close()

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

        print("Previous song")

    def __onNext(self, event):
        """Next song button has been clicked."""

        print("Next song")

    def __onPlay(self, event):
        """Play button has been clicked."""

        if self.__btnPlay.play == "play":
            self.__btnPlay.SetLabel(_('Play'))
            self.__menuPlayPlay.SetText(_('Play'))
            self.SetStatusText(_('Pause'))
            self.__btnPlay.play = "pause"
        else:
            self.__btnPlay.SetLabel(_('Pause'))
            self.__menuPlayPlay.SetText(_('Pause'))
            self.SetStatusText(_('Play'))
            self.__btnPlay.play = "play"

    def __onStop(self, event):
        """Stop to lay button has been clicked."""

        self.SetStatusText(_('Stop'))

        if self.__btnPlay.play == "play":
            self.__btnPlay.SetLabel(_('Play'))
            self.__menuPlayPlay.SetText(_('Play'))
            self.__btnPlay.play = "stop"

        print("Stop playing")

    def __onSettings(self, event):
        """"Menu tools, settings is clicked."""

        dialog = sDialog.SettingsDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def __onAbout(self, event):
        """Menu help, about is clicked."""

        wx.AboutBox(self.__aboutInfo)
