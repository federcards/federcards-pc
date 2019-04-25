#!/usr/bin/env python3

from .login import login
from .session import FederSession 


io = login()
#io = None

FederSession(io).run()

