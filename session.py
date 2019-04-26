#!/usr/bin/env python3

import os
import signal
from npyscreen import *
from .theme import FederTheme
import curses
from .card_extraction_observer import CardExtractionObserver

from .ui.main import FederMainForm
from .ui.change_password import FederChangePasswordForm







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
        self.registerForm("ChangePassword", FederChangePasswordForm(self))





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
