#!/usr/bin/env python3
import curses
from npyscreen import *


class FederChangePasswordForm(ActionPopup):

    DEFAULT_LINES = 15

    def __init__(self, parent):
        self.parent = parent
        self.io = parent.io
        ActionPopup.__init__(self, name="Change Password")

    def create(self):
        ActionPopup.create(self)
        prompt = [
            "You are about to change the card unlock password.",
            "",
            "This password will be used to encrypt all secrets",
            "stored, do not forget it, otherwise all data will",
            "be lost!",
            "If the self-destroy password is entered below,",
            "the card will be destroyed immediately.",

        ]
        self.prompt = self.add(Pager, values=prompt, height=len(prompt)+2)
        self.txtPassword1 = self.add(TitlePassword, name="New password")
        self.txtPassword2 = self.add(TitlePassword, name="Confirm again")

    def on_ok(self):
        if self.txtPassword1.value != self.txtPassword2.value:
            notify_wait("2 passwords do not match.")
            return
        password = self.txtPassword1.value
        if len(password) < 5:
            notify_wait("Please set a password with no less than 5 characters.")
            return
        self.txtPassword1.value = ""
        self.txtPassword2.value = ""
        if self.io.setPassword(password):
            notify_wait("Password changed successfully.")
        else:
            notify_wait("An error occured in changing password.")
        self.parent.switchForm("MAIN")

    def on_cancel(self):
        self.parent.switchForm("MAIN")
