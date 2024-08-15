# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Daniel Thompson

import wasp
import icons
import fonts


class HelloApp():

    NAME = 'Hello'
    ICON = icons.app

    def __init__(self, msg="Hello Emile -1 !"):
        self.msg = msg

    def foreground(self):
        self._draw()

    def _draw(self):
        draw = wasp.watch.drawable
        draw.fill()
        draw.string(self.msg, 0, 108, width=240)
