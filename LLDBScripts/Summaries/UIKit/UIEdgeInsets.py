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


class UIEdgeInsets_SynthProvider(SummaryBase.SummaryBase_SynthProvider):
    # typedef struct UIEdgeInsets {
    #     CGFloat top, left, bottom, right;
    # } UIEdgeInsets;
    def __init__(self, value_obj, internal_dict):
        super(UIEdgeInsets_SynthProvider, self).__init__(value_obj, internal_dict)

        self.top = None
        self.left = None
        self.bottom = None
        self.right = None

    def get_top(self):
        if self.top:
            return self.top

        self.top = self.get_child_value("top")
        return self.top

    def get_top_value(self):
        top = self.get_top()
        return float(top.GetValue())

    def get_left(self):
        if self.left:
            return self.left

        self.left = self.get_child_value("left")
        return self.left

    def get_left_value(self):
        left = self.get_left()
        return float(left.GetValue())

    def get_bottom(self):
        if self.bottom:
            return self.bottom

        self.bottom = self.get_child_value("bottom")
        return self.bottom

    def get_bottom_value(self):
        bottom = self.get_bottom()
        return float(bottom.GetValue())

    def get_right(self):
        if self.right:
            return self.right

        self.right = self.get_child_value("right")
        return self.right

    def get_right_value(self):
        right = self.get_right()
        return float(right.GetValue())
