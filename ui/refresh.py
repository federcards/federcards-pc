#!/usr/bin/env python3
import curses
from npyscreen import *

class FederEntry:

    PASSWORD = "PWD"
    HOTP = "HOTP"

    def __init__(self, nextmeta):
        assert nextmeta.typeof("NEXTMETA")
        index, entrytype, label = nextmeta.arguments[:3]

        self.index = int(index)
        self.entrytype = entrytype
        self.label = bytes.fromhex(label).decode("ascii") # TODO filter non-printable chars

        assert self.index > 0
        assert self.entrytype in [self.PASSWORD, self.HOTP]



class FederRefreshForm(FormBaseNew):

    DEFAULT_LINES = 6
    DEFAULT_COLUMNS = 40
    SHOW_ATX = 20
    SHOW_ATY = 10

    def __init__(self, parent):
        self.parent = parent
        self.io = parent.io
        FormBaseNew.__init__(self, name="Refreshing Entries")

    def create(self):
        FormBaseNew.create(self)
        self.prompt = self.add(Pager, height=2)

    def refreshEntries(self, *args):
        count = int(self.io("COUNT").arguments[0])
        self.prompt.values = ["Found %d items." % count, ""]
        self.display()

        refreshedList = []

        for i in range(0, count):
            try:
                newentry = FederEntry(self.io("NEXTMETA"))
            except:
                continue
            refreshedList.append(newentry)
            self.prompt.values[1] = "Downloading: %d of %d" % ((i+1, count))
            self.display()

        curses.napms(750)
        self.display()
        self.parent.home.wMain.values = refreshedList
        self.parent.switchForm("MAIN")
        self.parent.home.display()
