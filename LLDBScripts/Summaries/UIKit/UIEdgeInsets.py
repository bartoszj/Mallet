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


class UIEdgeInsets_SynthProvider(SummaryBase.SummaryBaseSyntheticProvider):
    # typedef struct UIEdgeInsets {
    #     CGFloat top, left, bottom, right;
    # } UIEdgeInsets;
    def __init__(self, value_obj, internal_dict):
        super(UIEdgeInsets_SynthProvider, self).__init__(value_obj, internal_dict)

        self.top = None
        self.left = None
        self.bottom = None
        self.right = None

    @Helpers.save_parameter("top")
    def get_top(self):
        return self.get_child_value("top")

    def get_top_value(self):
        return SummaryBase.get_float_value(self.get_top())

    @Helpers.save_parameter("left")
    def get_left(self):
        return self.get_child_value("left")

    def get_left_value(self):
        return SummaryBase.get_float_value(self.get_left())

    @Helpers.save_parameter("bottom")
    def get_bottom(self):
        return self.get_child_value("bottom")

    def get_bottom_value(self):
        return SummaryBase.get_float_value(self.get_bottom())

    @Helpers.save_parameter("right")
    def get_right(self):
        return self.get_child_value("right")

    def get_right_value(self):
        return SummaryBase.get_float_value(self.get_right())


def __lldb_init_module(debugger, dict):
    # UIEdgeInsets
    debugger.HandleCommand("type summary add -s \
            \"(top=${var.top}, left=${var.left}, bottom=${var.bottom}, right=${var.right})\" -v \
            --category UIKit UIEdgeInsets")

    debugger.HandleCommand("type category enable UIKit")
