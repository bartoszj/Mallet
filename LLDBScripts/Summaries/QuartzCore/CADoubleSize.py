#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Bartosz Janda
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


class CADoubleSize_SynthProvider(SummaryBase.SummaryBase_SynthProvider):
    # struct CADoubleSize {
    #     double width;
    #     double height;
    # };
    def __init__(self, value_obj, internal_dict):
        super(CADoubleSize_SynthProvider, self).__init__(value_obj, internal_dict)

        self.width = None
        self.height = None

    def get_width(self):
        if self.width:
            return self.width

        self.width = self.get_child_value("width", type_name="double", offset=0)
        return self.width

    def get_width_value(self):
        width = self.get_width()
        return float(width.GetValue())

    def get_height(self):
        if self.height:
            return self.height

        self.height = self.get_child_value("height", type_name="double", offset=8)
        return self.height

    def get_height_value(self):
        height = self.get_height()
        return float(height.GetValue())

    def summary(self):
        w = self.get_width_value()
        h = self.get_height_value()
        summary = "(width={}, height={})".format(self.formatted_float(w), self.formatted_float(h))
        return summary
