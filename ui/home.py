#!/usr/bin/env python3

import curses
from npyscreen import *
from .wgMultiselect import MultiSelectAction 


class FederHomeMenu(MultiSelectAction):

    def __init__(self, *args, **kvargs):
        MultiSelectAction.__init__(self, *args, **kvargs)

    def display_value(self, entry):
        return entry.entrytype + " | " + entry.label

class FederHomeForm(FormMutt):

    MAIN_WIDGET_CLASS = FederHomeMenu 
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
            "^A":             self.onAddEntry,
            "^P":             self.onChangePassword,
            "^R":             self.onRefresh,
            "^X":             self.onDelete,
        }
        self.wStatus1.value = " Feder Card Password Manager "
        self.wStatus2.value = " Actions "
        self.wCommand.value = "  ".join([
            "[Ctrl+A Add]",
            "[Ctrl+R Refresh]",
            "[Ctrl+X Delete]",
            "[Ctrl+P Change Password]",
            "[ESC Quit]",
        ])
        self.wMain.add_handlers(handlers)
        self.wMain.actionHighlighted = \
            lambda act, keypress: self.onItemSelection(act)

    def onKeypressESC(self, *args):
        if notify_yes_no(
            "Do you really want to exit the program?",
            title="Confirm",
            form_color="WARNING",
        ):
            self.parent.terminate()

    def onItemSelection(self, entry):
        if entry.entrytype == entry.HOTP:
            self.parent.switchForm("AccessTOTP")
            self.parent.accessTOTP.activateAccess(entry.index)
        elif entry.entrytype == entry.PASSWORD:
            self.parent.switchForm("AccessPassword")
            self.parent.accessPassword.activateAccess(entry.index)
            

    def onAddEntry(self, *args):
        self.parent.switchForm("Add")

    def onChangePassword(self, *args):
        self.parent.switchForm("ChangePassword")

    def onRefresh(self, *args):
        self.parent.switchForm("Refresh")
        self.parent.refresher.refreshEntries()

    def onDelete(self, *args):
        entries = self.wMain.get_selected_objects()
        count = len(entries)
        if count < 1: return
        if not notify_yes_no(
            "Sure to delete selected %d entr%s?" % (
                count,
                "ies" if count > 1 else "y"
            )
        ):
            return
        for entry in entries:
            self.io("DELENTRY=%d" % entry.index)
        self.parent.refresher.refreshEntries()

    def beforeEditing(self):
        if not self.initialEntriesGot:
            self.onRefresh()
            self.initialEntriesGot = True
