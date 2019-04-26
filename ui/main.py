#!/usr/bin/env python3

import curses
from npyscreen import *


class FederMainForm(FormMutt):

    MAIN_WIDGET_CLASS = MultiLineAction
    COMMAND_WIDGET_CLASS = FixedText

    def __init__(self, parent):
        self.parent = parent
        self.io = parent.io
        FormMutt.__init__(self)

    def __refreshEntries(self):
        count = int(self.io("COUNT").arguments[0])
        assert count >= 0
        self.count = count
        self.wMain.values = ["test", "test2"]
        for i in range(0, self.count):
            self.wMain.values.append(self.io("NEXTMETA"))
            
    def create(self):
        FormMutt.create(self)
        handlers = {
            curses.ascii.ESC: self.onKeypressESC,
            curses.ascii.CR:  self.onItemSelection,
            curses.ascii.NL:  self.onItemSelection,
            "^P":             self.onChangePassword,
        }
        self.wStatus1.value = " Feder Card Password Manager "
        self.wStatus2.value = " Actions "
        self.wCommand.value = "  ".join([
            "[Ctrl+A Add]",
            "[Ctrl+R Rename]",
            "[F5 Refresh]",
            "[Ctrl+P Change Password]",
            "[Ctrl+X Delete]",
            "[ESC Quit]",
        ])
        self.wMain.add_handlers(handlers)
        self.__refreshEntries()

    def onKeypressESC(self, *args):
        if notify_yes_no(
            "Do you really want to exit the program?",
            title="Confirm",
            form_color="WARNING",
        ):
            exit()

    def onItemSelection(self, *args):
        notify_wait(str(self.wMain.value))

    def onChangePassword(self, *args):
        self.parent.switchForm("ChangePassword")
