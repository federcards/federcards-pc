#!/usr/bin/env python3

import os
import signal
from npyscreen import *
from .theme import FederTheme
import curses
from .card_extraction_observer import CardExtractionObserver


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






class FederSession(NPSAppManaged):

    def __init__(self, io):
        NPSAppManaged.__init__(self)
        self.io = io
        self.setUpCardObserver()

    def setUpCardObserver(self):
        self.cardObserver = CardExtractionObserver(self.terminate)

    def terminate(self):
        # clean up as with <https://github.com/npcole/npyscreen/blob/master/npyscreen/npyssafewrapper.py>
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        # kill and no wait of anything
        os.kill(os.getpid(), signal.SIGKILL)

    def onStart(self):
        #setTheme(FederTheme)
        self.registerForm("MAIN", FederMainForm(self))





"""class FederShell(Cmd):
    
    intro = "Feder Card Password Manager v1"
    prompt = "(Feder Card) "

    def __init__(self, io):
        Cmd.__init__(self)
        self.io = io

    def __count(self):
        count = int(self.io("COUNT").arguments[0])
        assert count >= 0
        self.count = count

    def do_count(self, arg):
        self.__count()
        print("Got %d entries." % self.count)

    def do_quit(self, arg):
        "Exit this program."
        exit()

    def do_passwd(self, arg):
        "Updates password."
        password1 = getpass("Type new password for this card: ")
        password2 = getpass("Type this password again to confirm: ")
        if password1 != password2:
            print("2 passwords do not match. Password not changed.")
            return
        if self.io.setPassword(password1):
            print("Password changed.")
        else:
            print("Error occured changing password.")

    def do_all(self, arg):
        "List all entries."
        self.__count()
        for i in range(0, self.count):
            print(self.io("NEXTMETA"))

    def do_totp(self, arg):
        "Adds a Time-based One-time Password secret."
"""
