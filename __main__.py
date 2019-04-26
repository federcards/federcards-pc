#!/usr/bin/env python3

from .login import login
from .session import FederSession 
from threading import Timer


io = login()
FederSession(io).run()
