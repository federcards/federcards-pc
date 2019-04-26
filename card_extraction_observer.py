#!/usr/bin/env python3

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver




class CardExtractionObserver:

    def __init__(self, callback):
        self.callback = callback

        self.cardMonitor = CardMonitor()
        self.readerMonitor = ReaderMonitor()

        self.cardObserver = CardObserver()
        self.readerObserver = ReaderObserver()

        self.cardObserver.update = self.update
        self.readerObserver.update = self.update

        self.cardMonitor.addObserver(self.cardObserver)
        self.readerMonitor.addObserver(self.readerObserver)

    def update(self, observable, actions):
        added, removed = actions
        if removed:
            self.callback()
