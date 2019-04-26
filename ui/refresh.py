#!/usr/bin/env python3
import curses
from npyscreen import *

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

        for i in range(0, count):
            self.io("NEXTMETA")
            self.prompt.values[1] = "Downloading: %d of %d" % ((i+1, count))
            self.display()

        curses.napms(750)
        self.display()
        self.parent.switchForm("MAIN")
        self.parent.home.display()
