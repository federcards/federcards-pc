#!/usr/bin/env python3

class FedercardApplication:

    def __init__(self):
        self.widgetLogin = 
        self.widgetSession = 

    def __enter__(self, *a, **b):
        self.loop = urwid.MainLoop(self.widgetLogin)
        self.loop.start()

        self.widgetLogin.start()
        self.loop.widget = self.widgetSession
        self.loop.run()

    def __exit__(self, *a, **b):
        self.loop.stop()
