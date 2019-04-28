#!/usr/bin/env python3

import curses
from npyscreen import *
from .wgTOTP import FederTOTPPreviewField


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
