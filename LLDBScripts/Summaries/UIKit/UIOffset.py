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
import Helpers


class UIOffset_SynthProvider(SummaryBase.SummaryBaseSyntheticProvider):
    # typedef struct UIOffset {
    #     CGFloat horizontal, vertical;
    # } UIOffset;
    def __init__(self, value_obj, internal_dict):
        super(UIOffset_SynthProvider, self).__init__(value_obj, internal_dict)

        self.horizontal = None
        self.vertical = None

    @Helpers.save_parameter("horizontal")
    def get_horizontal(self):
        return self.get_child_value("horizontal")

    def get_horizontal_value(self):
        return get_float_value(self.get_horizontal())

    @Helpers.save_parameter("vertical")
    def get_vertical(self):
        return self.get_child_value("vertical")

    def get_vertical_value(self):
        return get_float_value(self.get_vertical())


def __lldb_init_module(debugger, dictionary):
    # UIOffset
    debugger.HandleCommand("type summary add -s \
            \"(horizontal=${var.horizontal}, vertical=${var.vertical})\" -v \
            --category UIKit UIOffset")

    debugger.HandleCommand("type category enable UIKit")
