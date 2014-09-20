#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2013 Bartosz Janda
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import SummaryBase


class UIOffset_SynthProvider(SummaryBase.SummaryBase_SynthProvider):
    # typedef struct UIOffset {
    #     CGFloat horizontal, vertical;
    # } UIOffset;
    def __init__(self, value_obj, internal_dict):
        super(UIOffset_SynthProvider, self).__init__(value_obj, internal_dict)

        self.horizontal = None
        self.vertical = None

    def get_horizontal(self):
        if self.horizontal:
            return self.horizontal

        self.horizontal = self.get_child_value("horizontal")
        return self.horizontal

    def get_horizontal_value(self):
        return self.get_float_value(self.get_horizontal())

    def get_vertical(self):
        if self.vertical:
            return self.vertical

        self.vertical = self.get_child_value("vertical")
        return self.vertical

    def get_vertical_value(self):
        return self.get_float_value(self.get_vertical())


def __lldb_init_module(debugger, dict):
    # UIOffset
    debugger.HandleCommand("type summary add -s \
            \"(horizontal=${var.horizontal}, vertical=${var.vertical})\" -v \
            --category UIKit UIOffset")

    debugger.HandleCommand("type category enable UIKit")
