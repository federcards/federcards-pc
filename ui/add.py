#!/usr/bin/env python3
import curses
from npyscreen import *
from .wgTOTP import FederTOTPPreviewField


class FederPreviewTOTPForm(ActionPopup):
    
    DEFAULT_COLUMNS = 65
    DEFAULT_LINES = 8
    
    def __init__(self, parent):
        self.parent = parent
        self.io = parent.io
        ActionPopup.__init__(self, name="Confirm TOTP Token")

    def create(self):
        ActionPopup.create(self)
        self.add(Pager, height=3, values=[
            "Use number below to check this credential with your service",
            "provider. If correct, choose <OK> to save.",
        ])
        self.previewer = self.add(FederTOTPPreviewField, parent=self)

    def activatePreview(self, secret):
        self.previewer.secret = secret
        self.previewer.activateUpdate()

    def on_ok(self):
        self.previewer.deactivateUpdate()

    def on_cancel(self):
        self.previewer.deactivateUpdate()
        self.parent.switchForm("Add")



class FederAddEntryForm(ActionPopup):

    DEFAULT_COLUMNS = 66 
    DEFAULT_LINES = 20
    
    def __init__(self, parent):
        self.parent = parent
        self.io = parent.io
        ActionPopup.__init__(self, name="Add Entry")

    def create(self):
        ActionPopup.create(self)

        self.prompt = self.add(
            Pager,
            values=[
                "You may save a password or a TOTP secret on card:",
                "",
                " * A password will be retrieved from card in a later time.",
                "   It can be copied to your clipboard, so you may paste that",
                "   into any service for authentication.",
                " * A TOTP secret, once written onto card, cannot be read out",
                "   again. You will only be able to get a 6 or 8 digit number",
                "   generated with this secret, with which you can sign-in to",
                "   Internet services.",
            ],
            height=10,
        )
        
        self.choiceType = self.add(
            TitleSelectOne,
            name="Entry Type",
            values=["Password", "TOTP secret for 2-factor authentication"],
            value=[0],
            height=3
        )
        self.txtName = self.add(TitleText, name="Entry Name", height=1)
        self.txtPassword = self.add(TitleText, name="Credential", height=1)

    def on_ok(self):
        selection = self.choiceType.value[0]
        if selection == 1:
            self.parent.previewTOTP.activatePreview(
                b"12345678901234567890")
            self.parent.switchForm("PreviewTOTP")
        else:
            
            notify_wait("abcd")


    def on_cancel(self):
        self.txtPassword.value = ""
        self.choiceType.value = [0]
        self.parent.switchForm("MAIN")
