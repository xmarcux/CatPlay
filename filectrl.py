#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import cPickle

propertyFile = "db" + os.sep + "CatPlay.properties"
categoryFile = "db" + os.sep + "CatPlay.categories"

def getProperties():
    """
    Returns properties saved in file
    as a dictionary.
    If file not correct an empty
    dict is returned.
    """


    if os.path.exists(propertyFile):
        fileCont = ""
        try:
            fileCont = cPickle.load(open(propertyFile, 'rb'))
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
    cPickle.dump(fileCont, open(propertyFile, 'wb'))


def getCategories():
    """
    Returns categories saved in file
    as a dictionary.
    If file is not correct an empty
    disc is returned.
    """

    if os.path.exists(categoryFile):
        contFile = ""
        try:
            contFile = cPickle.load(open(categoryFile, 'rb'))
        except:
            contFile = {}

        if isinstance(contFile, dict):
            return contFile
        else:
            return {}
    else:
        return {}

def addCategory(catChar, newCat):
    """
    Adds a new category
    to existing categories and 
    saves to file.
    """

    #check if it alreaty exists if it does replace it
    cat = getCategories()
    cat[catChar] = newCat
    cPickle.dump(cat, open(categoryFile, 'wb'))

def deleteCategory(delCat):
    """
    Deletes given category,
    saves new dict to file and
    returns changed dict.
    """

    cat = getCategories()

    for (k, v) in cat.iteritems():
        if v == delCat:
            del cat[k]
            break;

    cPickle.dump(cat, open(categoryFile, 'wb'))

    return cat

def getMusicFiles():
    """
    Reads music files from music
    directory specified in properties.
    Puts filenames in arrays sorted by 
    category.
    Returns a dict with category keys
    and arrays as values.
    """

    prop = getProperties()
    cat = getCategories()
    musicFiles = {}
    if ("musicDir" in prop) and ("fileToken" in prop):
        for root, dirs, files in  os.walk(prop["musicDir"]):
            for f in files:
                ending =  os.path.splitext(f)[1] 
                if ending == ".ogg" or ending == ".mp3" or ending == ".wav" or ending == ".m4a":
                    if prop["fileToken"]:
                        fSplit = f.split(prop["fileToken"])
                        if len(fSplit) == 4 and fSplit[0].isdigit():
                            fTokens = list(fSplit[1])
                            for t in fTokens:
                                if t in cat:
                                    if cat[t] in musicFiles:
                                        musicFiles[cat[t]] = musicFiles[cat[t]] + [root + os.sep + f]
                                    else:
                                        musicFiles[cat[t]] = [root + os.sep + f]
                                else:
                                    if "noSpecCategory" in musicFiles:
                                        musicFiles["noSpecCategory"] = musicFiles["noSpecCategory"] + [root + os.sep + f]
                                    else:
                                        musicFiles["noSpecCategory"] = [root + os.sep + f]

        return musicFiles
    else: 
        return {}
