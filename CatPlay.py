#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ui.mainWindow
import gettext

import wx.media as m
import time

gettext.install('CatPlay', '/locale' , unicode=False)

if __name__ == '__main__':
    app = wx.App(False)
    mainW = ui.mainWindow.MainWindow()
    #frame = wx.Frame(None, -1, "Category Play", size = (320, 350))
    """    cntl = m.MediaCtrl(parent=mainW)
    if cntl.Load('/home/marcux/projects/CatPlay/db/song.ogg'):
        print('Song loaded')
    else:
        print('Error loading song')

    cntl.Play()

    vol = 1.0
    while vol > 0.0:
        time.sleep(0.5)
        cntl.SetVolume(vol)
        vol -= 0.1

    cntl.Stop()
    if cntl.Load('/home/marcux/projects/CatPlay/db/Intervall.wav'):
        print(".wav loaded")
    else:
        print("Error loading wav")

    cntl.Play()

    while vol < 1.0:
        time.sleep(0.5)
        cntl.SetVolume(vol)
        vol += 0.1
    """


    #frame.Show()

    app.MainLoop()
