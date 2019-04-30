#!/usr/bin/env python3
import curses
from npyscreen import *


class FederDeleteForm(ActionPopup):

    def __init__(self, parent):
        self.parent = parent
        self.io = parent.io
        ActionPopup.__init__(self)

    def create(self):
        ActionPopup.create(self)
        
