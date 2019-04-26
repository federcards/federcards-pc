#!/usr/bin/env python3

from npyscreen import npysThemeManagers as ThemeManagers
from curses import *

class FederTheme(ThemeManagers.ThemeManager):
    _colors_to_define = (
        ("WHITE_BLUE",  COLOR_WHITE,        -1),
        ("WHITE_RED",   COLOR_WHITE,        COLOR_RED),
        ("WHITE_ON_DEFAULT",    COLOR_WHITE, -1     ),
    )

    default_colors = {
        'DEFAULT'     : 'WHITE_BLUE',
        'FORMDEFAULT' : 'BLACK_WHITE',
        'NO_EDIT'     : 'BLUE_WHITE',
        'STANDOUT'    : 'BLACK_WHITE',
        'CURSOR'      : 'BLACK_WHITE',
        'CURSOR_INVERSE': 'WHITE_BLACK',
        'LABEL'       : 'WHITE_ON_DEFAULT',
        'LABELBOLD'   : 'BLACK_WHITE',
        'CONTROL'     : 'BLUE_WHITE',
        'WARNING'     : 'WHITE_RED',
        'CRITICAL'    : 'BLACK_RED',
        'GOOD'        : 'GREEN_BLACK',
        'GOODHL'      : 'GREEN_WHITE',
        'VERYGOOD'    : 'WHITE_GREEN',
        'CAUTION'     : 'YELLOW_WHITE',
        'CAUTIONHL'   : 'BLACK_YELLOW',
    }

    def __init__(self, *args, **keywords):
        use_default_colors()
        ThemeManagers.ThemeManager.__init__(self, *args, **keywords)
