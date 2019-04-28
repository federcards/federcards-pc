#!/usr/bin/env python3
import curses
from npyscreen import *
import base64
import math

from .wgTOTP import FederTOTPPreviewField


def addToCard(io, name, password, isHOTP=False):
    command = "ADDHOTPENTRY" if isHOTP else "ADDPWDENTRY"
    addret = io(command)
    if not (addret.typeof("ADDHOTPENTRY") or addret.typeof("ADDPWDENTRY")):
        notify_wait("Failed to create new entry.\n" + str(addret))
        return False

    try:
        newid = int(addret.arguments[0])
        if type(name) == str: name = name.encode("ascii")
        if type(password) == str: password = password.encode("ascii")
        assert type(name) == bytes and type(password) == bytes and newid > 0
    except:
        notify_wait(
            "Wrong parameter in creating new entry. Contact program author.")
        return False

    try:
        dataret = io("SETDATA=%d,%s" % (newid, password.hex()))
        nameret = io("SETMETA=%d,%s" % (newid, name.hex()))
        assert dataret.typeof("OK") and nameret.typeof("OK")
    except Exception as e:
        notify_wait("Failure writing entry data to card.\n" + str(e))
        return False

    return True




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

    def activatePreview(self, name, secret):
        self.__entryName = name
        self.__entrySecret = secret
        self.previewer.secret = secret
        self.previewer.activateUpdate()

    def on_ok(self):
        self.previewer.deactivateUpdate()
        # write to card
        secret = self.previewer.secret
        self.previewer.secret = b""
        # do write
        success = addToCard(
            self.io,
            name=self.__entryName,
            password=self.__entrySecret,
            isHOTP=True
        )
        # on success, clear all forms and return
        if success:
            self.parent.add.clearForm()
            self.parent.switchForm("MAIN")
            self.parent.home.onRefresh()
        else:
            self.on_cancel()

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
        credential = self.txtPassword.value
        label = self.txtName.value
        if not (0 < len(label) <= 100 and 0 < len(credential) <= 100):
            notify_wait(
                "Invalid input.\n" +
                "Both entry label and password must not be empty or exceeding 100 chars."
            )
            return

        if selection == 1:
            secret = credential.strip().upper().encode("ascii")
            secret += ( math.ceil(len(secret) / 8) * 8 - len(secret) ) * b"="
            try:
                secret = base64.b32decode(secret)
            except:
                notify_wait("This credential is not valid for TOTP use.\n" + secret.decode("ascii"))
                return

            self.parent.previewTOTP.activatePreview(label, secret)
            self.parent.switchForm("PreviewTOTP")
        else:
            
            notify_wait("abcd")

    def clearForm(self):
        self.txtName.value = ""        
        self.txtPassword.value = ""
        self.choiceType.value = [0]

    def on_cancel(self):
        self.clearForm()
        self.parent.switchForm("MAIN")
