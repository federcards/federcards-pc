#!/usr/bin/env python3

import os
import signal
from npyscreen import *
from .theme import FederTheme
import curses

from .ui.home import FederHomeForm
from .ui.change_password import FederChangePasswordForm
from .ui.refresh import FederRefreshForm
from .ui.add import FederAddEntryForm, FederPreviewTOTPForm
from .card_extraction_observer import CardExtractionObserver
from .cardio import CardIO






class FederSession(NPSAppManaged):

    def __init__(self, io):
        NPSAppManaged.__init__(self)
        self.io = io
        self.setUpCardObserver()
        self.initialEntriesGot = False

    def setUpCardObserver(self):
        self.cardObserver = CardExtractionObserver(lambda: self.terminate(True))

    def terminate(self, kill=False):
        # clean up as with <https://github.com/npcole/npyscreen/blob/master/npyscreen/npyssafewrapper.py>
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        # kill and no wait of anything
        os.kill(os.getpid(), signal.SIGKILL if kill else signal.SIGTERM)

    def onStart(self):
        #setTheme(FederTheme)
        self.refresher = FederRefreshForm(self)
        self.home = FederHomeForm(self)
        self.previewTOTP = FederPreviewTOTPForm(self)

        self.registerForm("Refresh", self.refresher)
        self.registerForm("ChangePassword", FederChangePasswordForm(self))
        self.registerForm("Add", FederAddEntryForm(self))
        self.registerForm("PreviewTOTP", self.previewTOTP)
        self.registerForm("MAIN", self.home)



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
