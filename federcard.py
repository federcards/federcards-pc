#!/usr/bin/env python3

import os
import sys
import subprocess
from threading import Thread

def reader(f,buf):
   while True:
     line = f.readline()
     if line:
        buf.append(line)
     else:
        break


class ATShell:

    def __init__(self):
        self.__p = subprocess.Popen(
            ["mono", "./atshell.exe"], 
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            bufsize=0
        )

    def __enter__(self, *a, **b):
        self.__atoutput = []
        self.__reader = Thread(
            target=reader, args=(self.__p.stdout, self.__atoutput)
        )
        self.__reader.start()
        return self

    def __exit__(self, *a, **b):
        self.__p.terminate()

    def poll(self):
        if len(self.__atoutput) > 1:
            x = self.__atoutput.pop(0).strip()
            if x:
                return x.decode("ASCII")
            else:
                return None
        else:
            if self.__p.returncode is not None:
                raise Exception("AT shell terminated.")
            return None

    def put(self, string):
        if self.__p.returncode is not None:
            raise Exception("AT shell terminated.")
        print(">> " + string)
        self.__p.stdin.write(string.encode("ascii") + b"\r\n")


if __name__ == "__main__":
    import time

    atshellStarted = False

    with ATShell() as x:
        while True:
            nl = x.poll()
            if nl:
                print(nl)
            else:
                time.sleep(0.1)
                continue

            if nl == "!PASSWORD_HEX":
                x.put("46454445522043415244")

            if nl == "!ATSHELL_START":
                atshellStarted = True

            if atshellStarted:
                x.put("AT+STATUS")
                time.sleep(0.1)
