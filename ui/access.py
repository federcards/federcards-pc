#!/usr/bin/env python3

import curses
from threading import Thread
import time
from npyscreen import *
import pyperclip
from .wgTOTP import FederTOTPPreviewField

class FederPasswordAccessForm(FormBaseNew):
    
    DEFAULT_LINES = 8
    DEFAULT_COLUMNS = 70
    SHOW_ATX = 10
    SHOW_ATY = 10

    PASSWORD_CACHE_TIME = 20

    def __init__(self, parent):
        self.parent = parent
        self.io = self.parent.io
        FormBaseNew.__init__(self, name="Password Access")
        self.currentAccessIndex = None
        self.timer = Thread(target=self.timedLoop)
        self.timer.start()

    def timedLoop(self):
        cachedIndex = None
        countdown = 0
        while True:
            if self.currentAccessIndex is not None:
                if cachedIndex != self.currentAccessIndex:
                    cachedIndex = self.currentAccessIndex
                    countdown = self.PASSWORD_CACHE_TIME
                else:
                    countdown -= 1
                if countdown <= 0:
                    cachedIndex = None
                    self.on_ok()
            else:
                cachedIndex = None
            time.sleep(1)

    def create(self):
        FormBaseNew.create(self)
        self.prompt = self.add(Pager, values=[
            "Password is now copied to your clipboard.",
            "Valid for %d seconds. After that clipboard will be cleared." % \
            self.PASSWORD_CACHE_TIME,
        ], height=3)
        self.closer = self.add(
            Button,
            name="PRESS <ENTER> TO CLEAR UP IMMEDIATELY"
        )
        self.closer.add_handlers({
            curses.ascii.CR: self.on_ok,
            curses.ascii.NL: self.on_ok,
            curses.ascii.ESC: self.on_ok
        })

    def __writeClipboard(self, password):
        pyperclip.copy(password)

    def on_ok(self, *args):
        self.__writeClipboard("")
        self.currentAccessIndex = None
        self.parent.switchForm("MAIN")
        self.parent.home.display()

    def activateAccess(self, index):
        password = self.io("GETDATA=%d" % index)
        success = False
        if password.typeof("EMPTY_ENTRY"):
            notify_wait("This entry is empty. Please edit or delete.")
        elif password.typeof("UNLOCK_REQUIRED"):
            notify_wait("The card is not unlocked yet.")
        elif password.typeof("GETDATA"):
            if password.arguments[0] != 'PWDHEX':
                notify_wait("This is not a password entry. Contact author.")
            else:
                try:
                    password = bytes.fromhex(
                        password.arguments[1]).decode("ascii")
                    success = True
                except:
                    notify_wait("This password is non-printable.")
        if not success:
            self.parent.switchForm("MAIN")
        self.__writeClipboard(password)
        self.currentAccessIndex = index


class FederTOTPAccessForm(FormBaseNew):

    DEFAULT_LINES = 8
    DEFAULT_COLUMNS = 40
    SHOW_ATX = 10
    SHOW_ATY = 10

    def __init__(self, parent):
        self.parent = parent
        self.io = self.parent.io
        FormBaseNew.__init__(self, name="TOTP Access")

    def create(self):
        FormBaseNew.create(self)
        self.prompt = self.add(Pager, values=[
            "Time-based One-Time Password:"
        ], height=3)
        self.totp = self.add(FederTOTPPreviewField, parent=self.parent)
        self.totp.add_handlers({
            curses.ascii.CR: self.on_ok,
            curses.ascii.NL: self.on_ok,
            curses.ascii.ESC: self.on_ok
        })

    def activateAccess(self, entryID):
        self.totp.source = entryID
        self.totp.activateUpdate()

    def on_ok(self, *args):
        self.totp.deactivateUpdate()
        self.parent.switchForm("MAIN")
