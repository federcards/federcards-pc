#!/usr/bin/env python3

import curses
from npyscreen import *


class FederHomeForm(FormMutt):

    MAIN_WIDGET_CLASS = MultiLineAction
    COMMAND_WIDGET_CLASS = FixedText

    def __init__(self, parent):
        self.parent = parent
        self.io = parent.io
        self.initialEntriesGot = False
        FormMutt.__init__(self)

    def create(self):
        FormMutt.create(self)
        handlers = {
            curses.ascii.ESC: self.onKeypressESC,
            curses.ascii.CR:  self.onItemSelection,
            curses.ascii.NL:  self.onItemSelection,
            "^P":             self.onChangePassword,
            "^R":             self.onRefresh,
        }
        self.wStatus1.value = " Feder Card Password Manager "
        self.wStatus2.value = " Actions "
        self.wCommand.value = "  ".join([
            "[Ctrl+A Add]",
            "[Ctrl+E Edit]",
            "[Ctrl+R Refresh]",
            "[Ctrl+X Delete]",
            "[Ctrl+P Change Password]",
            "[ESC Quit]",
        ])
        self.wMain.add_handlers(handlers)

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

    def onRefresh(self, *args):
        self.parent.switchForm("Refresh")
        self.parent.refresher.refreshEntries()


    def beforeEditing(self):
        if not self.initialEntriesGot:
            self.onRefresh()
            self.initialEntriesGot = True
