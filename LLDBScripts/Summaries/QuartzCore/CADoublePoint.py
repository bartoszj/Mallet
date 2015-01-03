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
import Helpers


class CADoublePoint_SynthProvider(SummaryBase.SummaryBaseSyntheticProvider):
    # struct CADoublePoint {
    #     double x;
    #     double y;
    # };
    def __init__(self, value_obj, internal_dict):
        super(CADoublePoint_SynthProvider, self).__init__(value_obj, internal_dict)

        self.x = None
        self.y = None

    @Helpers.save_parameter("x")
    def get_x(self):
        return self.get_child_value("x", type_name="double", offset=0)

    def get_x_value(self):
        return self.get_float_value(self.get_x())

    def get_x_summary(self):
        x = self.get_x_value()
        return None if x is None else "x={}".format(self.formatted_float(x))

    @Helpers.save_parameter("y")
    def get_y(self):
        return self.get_child_value("y", type_name="double", offset=8)

    def get_y_value(self):
        return self.get_float_value(self.get_y())

    def get_y_summary(self):
        y = self.get_y_value()
        return None if y is None else "y={}".format(self.formatted_float(y))

    def summary(self):
        summary = "({}, {})".format(self.get_x_summary(), self.get_y_summary())
        return summary
