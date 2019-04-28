#!/usr/bin/env python3

import os
import signal
from npyscreen import *
from .theme import FederTheme
import curses

from .ui.home import FederHomeForm
from .ui.change_password import FederChangePasswordForm
from .ui.refresh import FederRefreshForm
from .ui.access import *
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
        self.accessTOTP = FederTOTPAccessForm(self)
        self.add = FederAddEntryForm(self)

        self.registerForm("Refresh", self.refresher)
        self.registerForm("ChangePassword", FederChangePasswordForm(self))
        self.registerForm("Add", self.add)
        self.registerForm("PreviewTOTP", self.previewTOTP)
        self.registerForm("AccessTOTP", self.accessTOTP)
        self.registerForm("MAIN", self.home)
