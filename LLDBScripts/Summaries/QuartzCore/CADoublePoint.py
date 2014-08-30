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


class CADoublePoint_SynthProvider(SummaryBase.SummaryBase_SynthProvider):
    # struct CADoublePoint {
    #     double x;
    #     double y;
    # };
    def __init__(self, value_obj, internal_dict):
        super(CADoublePoint_SynthProvider, self).__init__(value_obj, internal_dict)

        self.x = None
        self.y = None

    def get_x(self):
        if self.x:
            return self.x

        self.x = self.get_child_value("x", type_name="double", offset=0)
        return self.x

    def get_x_value(self):
        x = self.get_x()
        return float(x.GetValue())

    def get_y(self):
        if self.y:
            return self.y

        self.y = self.get_child_value("y", type_name="double", offset=8)
        return self.y

    def get_y_value(self):
        y = self.get_y()
        return float(y.GetValue())

    def summary(self):
        x = self.get_x_value()
        y = self.get_y_value()
        summary = "(x={}, y={})".format(self.formatted_float(x), self.formatted_float(y))
        return summary
