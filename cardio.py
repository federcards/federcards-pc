#!/usr/bin/env python3

import hashlib

def derivePassword(password):
    if type(password) == str: password = password.encode("ascii")
    return hashlib.scrypt(
        password=password,
        salt=b"feder.cards/pm1",
        n=65536,
        r=8,
        p=8,
        maxmem=128*1024*1024,
        dklen=32
    ).hex().encode("ascii")


class ATResponse:

    def __init__(self, what):
        self.__orig = what
        self.__parse()

    def __parse(self):
        if self.__orig.startswith("+"):
            cmdName, cmdArgs = self.__orig[1:].split(":")[:2]
        else:
            cmdName = self.__orig
            cmdArgs = ""
        self.__cmdName = cmdName
        self.__cmdArgs = cmdArgs.split(",")

    def __str__(self):
        return self.__orig

    @property
    def command(self):
        return self.__cmdName

    @property
    def arguments(self):
        return self.__cmdArgs

    def __eq__(self, other):
        return str(self) == str(other)

    def typeof(self, other):
        return self.command.lower() == other.lower()



class CardIO:

    def __init__(self, cardService):
        self.cardService = cardService

    def __call__(self, command):
        if type(command) == str:
            command = command.encode("ascii")
        assert type(command) == bytes
        if not command.startswith(b"AT+"):
            command = b"AT+" + command
        data = list(command)
        apdu = [0x88, 0x00, 0x00, 0x00, len(data)] + data + [0xFE]

        response, sw1, sw2 = self.cardService.connection.transmit(apdu)
        return ATResponse(bytes(response).decode("ascii"))

    def factoryReset(self, selfDestroyPassword):
        selfDestroyPassword = derivePassword(selfDestroyPassword)
        apdu = [0x88, 0x88, 0x00, 0x00, len(selfDestroyPassword)] +\
            list(selfDestroyPassword)
        response, sw1, sw2 = self.cardService.connection.transmit(apdu)
        return sw1, sw2

    def setPassword(self, newPassword):
        status = self("STATUS").arguments[0]
        if status == "UNINITIALIZED" or status == "UNLOCKED":
            print("Setting card password.")
            return self(b"SETPWD=" + derivePassword(newPassword)).typeof("ok")
        else:
            return False

    def lock(self):
        return self(b"LOCK").typeof("ok")

    def unlock(self, password):
        return self(b"UNLOCK=" + derivePassword(password))
