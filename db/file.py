#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import cPickle

filename = "db" + os.sep + "CatPlay.properties"

def getProperties():
    """
    Returns properties saved in file
    as a dictionary.
    If file not correct an empty
    dict is returned.
    """


    if os.path.exists(filename):
        fileCont = ""
        try:
            fileCont = cPickle.load(open(filename, 'rb'))
        except:
            fileCont = {}

        if isinstance(fileCont, dict):
            return fileCont
        else:
            return {}
    else:
        return {}

def setProperty(name, value):
    """
    Writes a property to
    property file.
    """

    fileCont = getProperties()
    fileCont[name] = value
    cPickle.dump(fileCont, open(filename, 'wb'))
