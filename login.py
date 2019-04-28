#!/usr/bin/env python3

import time

from getpass import getpass
from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest

from .cardio import CardIO



def login(factoryReset=False):
    print("Waiting for card...")
    cardRequest = CardRequest(timeout=10) #, cardType=cardtype)
    cardService = cardRequest.waitforcard()

    cardService.connection.connect()
    atr = ATR(cardService.connection.getATR())
    identification = bytes(atr.getHistoricalBytes())

    if identification != b"feder.cards/pm1":
        print("Wrong card inserted.")
        print("Please insert a Feder Card Password Manager v1.")
        exit()

    cardIO = CardIO(cardService)

    #return cardIO # XXX debug

    # 1. Check status

    if not factoryReset:
        status = cardIO("STATUS")
        if status.arguments[0] == "UNINITIALIZED":
            factoryReset = True
            print("Card is not initialized. This must be done before any use.")

    if factoryReset:
        print("Please set a self-destroy password.")
        print("This password is set only once. It is NOT used for unlocking a card, but for DESTROYING a card if you are forced to give the password.")

        while True:
            resetPassword1 = getpass("Password for destroying card:")
            resetPassword2 = getpass("Type again for confirm:")
            if resetPassword1 == resetPassword2: break
            print("Passwords do not match. Try again, or Ctrl+C to exit.")
        print("Resetting card...")
        print(cardIO.factoryReset(resetPassword1))
        print("Setting default password.")
        print(cardIO.setPassword("default"))
        print("Done with factory reset.")

    # 2. Ask for password and unlock the card

    status = cardIO("STATUS")
    if status.arguments[0] == "LOCKED":
        print("Card is locked. Type in a password to unlock.")
        print("Default password after factory reset is 'default'.")
        print("If you used up all attempts for unlock, the card is destroyed!")
        while True:        
            attempts = int(cardIO("ATTEMPTS").arguments[0])
            password = getpass("Input password. Remaining attempts: %d > " % attempts)
            if attempts > 0:
                unlockResult = cardIO.unlock(password)
                if unlockResult.typeof("ok") or unlockResult.typeof("already_unlocked"):
                    break
                elif unlockResult.typeof("e2prom_wrong_password"):
                    print("Wrong password.")
                else:
                    break
            else:
                break
    
    if cardIO("STATUS").arguments[0] == "UNINITIALIZED":
        print("Card reports uninitialized. Please re-start this program.")
        exit()

    if not cardIO("STATUS").arguments[0] == "UNLOCKED":
        print("Card unlocking failed. Restart this program.")
        exit()


    return cardIO
