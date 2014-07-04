#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import settingsDialog as sDialog

class MainWindow (wx.Frame):
    """Main window for application."""

    def __init__(self):
        """Init function."""

        wx.Frame.__init__(self, None, title=_('Cat Play'), size=(300, 300))
        self.__panel = wx.Panel(self, wx.ID_ANY)

        self.CreateStatusBar()
        self.SetMenuBar(self.__createMenu())

        self.__setupAboutInfo()

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
        playPlay = playMenu.Append(wx.ID_YES, _('&Play'), _('Plays current song'))
        self.Bind(wx.EVT_MENU, self.__onPlay, playPlay)
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

        print("Add category to library")

    def __onDeleteCategory(self, event):
        """Removes category from library"""

        print("Removes category from library")

    def __onPrevious(self, event):
        """Previous song button has been clicked."""

        print("Previous song")

    def __onNext(self, event):
        """Next song button has been clicked."""

        print("Next song")

    def __onPlay(self, event):
        """Play button has been clicked."""

        print("Play")

    def __onStop(self, event):
        """Stop to lay button has been clicked."""

        print("Stop playing")

    def __onSettings(self, event):
        """"Menu tools, settings is clicked."""

        dialog = sDialog.SettingsDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def __onAbout(self, event):
        """Menu help, about is clicked."""

        wx.AboutBox(self.__aboutInfo)
