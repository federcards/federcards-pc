#!/usr/bin/env python3

import curses
from npyscreen import *
from threading import Thread
import time
import sys
import struct


class FederTOTPPreviewField(Textfield):

    def __init__(self, *args, **kvargs):
        self.parent = kvargs["parent"]
        self.io = self.parent.io
        del kvargs["parent"]
        kvargs["value"] = "(LOADING...WAIT...)"
        self.secret = None 
        self.source = None 
        self.updating = False

        self.oldTimestamp = ""
        
        Textfield.__init__(self, *args, **kvargs)

        self.updatingThread = Thread(target=self.updateCalculation)
        self.updatingThread.start()

    def updateFromCard(self, timestamp):   
        if self.secret is not None:
            assert type(self.secret) == bytes
            return self.io(
                b"TESTHOTP=" + self.secret.hex().encode("ascii") +\
                b"," + timestamp).arguments[0]
        if self.source is not None:
            assert type(self.source) == int
            ret = self.io(b"GETDATA=%d,%s,8" % (self.source, timestamp))
            if ret.typeof("GETDATA") and ret.arguments[0] == "HOTP":
                return ret.arguments[1]
            return "ERROR::%s" % ret.command
        return "ERROR"
        
    def activateUpdate(self):
        self.oldTimestamp = ""
        self.value = "(LOADING...WAIT...)"
        self.display()
        self.updating = True

    def deactivateUpdate(self):
        self.updating = False

    def updateCalculation(self):
        # runs in a separate thread
        while True:
            timestamp = struct.pack(
                ">q", int(time.time() / 30)).hex().encode("ascii")
            if timestamp != self.oldTimestamp:
                if self.updating:
                    self.value = self.updateFromCard(timestamp)
                    self.display()
                    self.oldTimestamp = timestamp
            time.sleep(0.5)

