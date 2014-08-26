#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import filectrl

class AddCategoryDialog(wx.Dialog):
    """
    This class is a dialog 
    to add categories for 
    the music files.
    """

    def __init__(self, *args, **kw):
        """Initialization."""

        super(AddCategoryDialog, self).__init__(*args, **kw)

        self.SetTitle(_('Add category'))
        self.__createView()

    def __createView(self):
        """Method creates the view of the dialog."""

        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer.Add(inputSizer, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(topSizer, 0, wx.ALL | wx.EXPAND, 5)

        #Category name
        catSizer = wx.BoxSizer(wx.HORIZONTAL)
        catText = wx.StaticText(panel, wx.ID_ANY, _('Category name:'))
        catSizer.Add(catText, 0, wx.ALL, 5)
        self.__catInput = wx.TextCtrl(panel, wx.ID_ANY)
        catSizer.Add(self.__catInput, 1, wx.ALL | wx.EXPAND, 5)
        inputSizer.Add(catSizer, 1, wx.ALL | wx.EXPAND, 5)

        #Category token
        tokenSizer = wx.BoxSizer(wx.HORIZONTAL)
        tokenText = wx.StaticText(panel, wx.ID_ANY, _('Category character for filename:'))
        tokenSizer.Add(tokenText, 0, wx.ALL, 5)
        self.__tokenInput = wx.TextCtrl(panel, wx.ID_ANY)
        self.__tokenInput.SetMaxLength(1)
        tokenSizer.Add(self.__tokenInput, 0, wx.ALL | wx.EXPAND, 5)
        inputSizer.Add(tokenSizer, 1, wx.ALL | wx.EXPAND, 5)
         
        #Buttons
        mainSizer.Add(wx.StaticLine(panel, wx.ID_ANY), 0, wx.ALL | wx.EXPAND, 5)
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

    def __onSave(self, event):
        """Save button is clicked."""

        categories = filectrl.getCategories()
        catInput = self.__catInput.GetValue()
        tokenInput = self.__tokenInput.GetValue()

        error_msg = ""
        if catInput == "":
            error_msg = _("Specify category name.\n")

        if catInput in categories.values():
            error_msg += _("Category does already exist.\n Specify a new name.")

        if tokenInput == "":
            error_msg += _("Specify category character.")

        if tokenInput in categories:
            error_msg += _("Category character does alreay exists.\n Specify a new character.")

        if error_msg:
            error_msg = "Error saving new category:\n\n" + error_msg
            dialog = wx.MessageDialog(self, error_msg, _('Error saving'), wx.OK | wx.ICON_ERROR)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            filectrl.addCategory(self.__tokenInput.GetValue(), self.__catInput.GetValue())
            self.GetParent().updateCategories()
            self.Destroy()

    def __onCancel(self, event):
        """Cancel button is clicked."""

        self.Destroy()




class DeleteCategoryDialog(wx.Dialog):
    """
    This class is a dialog
    to delete categories for
    the music files.
    """

    def __init__(self, *args, **kw):
        """Initialization."""

        super(DeleteCategoryDialog, self).__init__(*args, **kw)

        self.SetTitle(_('Delete category'))
        self.__createView()

    def __createView(self):
        """Method creates the view of the dialog."""

        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(inputSizer, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(topSizer, 0, wx.ALL | wx.EXPAND, 5)

        #Delete input
        delText = wx.StaticText(panel, wx.ID_ANY, _('Choose category to delete:'))
        inputSizer.Add(delText, 0, wx.ALL | wx.EXPAND, 5)
        
        #Get categories from file
        cat = filectrl.getCategories().values()

        cat.sort()
        categories = cat

        if len(categories):
            self.__delCombo = wx.ComboBox(panel, wx.ID_ANY, style=wx.CB_READONLY,
                                          value=categories[0], choices=categories)
        else:
            self.__delCombo = wx.ComboBox(panel, wx.ID_ANY, style=wx.CB_READONLY,
                                          choices=categories)

        inputSizer.Add(self.__delCombo, 1, wx.ALL | wx.EXPAND, 5)

        #buttons
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        deleteBtn = wx.Button(panel, wx.ID_ANY, _('&Delete'))
        self.Bind(wx.EVT_BUTTON, self.__onDelete, deleteBtn)
        btnSizer.Add(deleteBtn, 0, wx.ALL, 5)
        cancelBtn = wx.Button(panel, wx.ID_ANY, _('&Cancel'))
        self.Bind(wx.EVT_BUTTON, self.__onCancel, cancelBtn)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)

        mainSizer.Add(wx.StaticLine(panel, wx.ID_ANY), 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(btnSizer, 0, wx.BOTTOM | wx.ALIGN_CENTER, 5)

        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

    def __onCancel(self, event):
        """Cancel button is clicked."""

        self.Destroy()

    def __onDelete(self, event):
        """Delete button is clicked."""

        if self.__delCombo.GetCount():
            catTxt = self.__delCombo.GetValue()
            dialog = wx.MessageDialog(self, _('Do you want to delete category: ') + 
                                      catTxt, _('Delete'), 
                                      wx.YES_NO | wx.ICON_QUESTION)

            if wx.ID_YES == dialog.ShowModal():
                #delete category from file and update combo
                newCats = filectrl.deleteCategory(catTxt).values()

                newCats.sort()
                if len(newCats):
                    self.__delCombo.SetItems(newCats)
                    self.__delCombo.SetSelection(0)
                else:
                    self.__delCombo.Clear()
                    self.__delCombo.SetValue("")

                self.GetParent().updateCategories()

                confirm = wx.MessageDialog(self, _('Category successfully deleted: ') +
                                           catTxt, _('Deleted'),
                                           wx.OK | wx.ICON_INFORMATION)
                confirm.ShowModal()
