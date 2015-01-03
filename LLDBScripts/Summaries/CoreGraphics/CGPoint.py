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


class CGPoint_SynthProvider(SummaryBase.SummaryBaseSyntheticProvider):
    # struct CGPoint {
    #   CGFloat x;
    #   CGFloat y;
    # };
    # typedef struct CGPoint CGPoint;
    def __init__(self, value_obj, internal_dict):
        super(CGPoint_SynthProvider, self).__init__(value_obj, internal_dict)

        self.x = None
        self.y = None

    @Helpers.save_parameter("x")
    def get_x(self):
        return self.get_child_value("x")

    def get_x_value(self):
        return self.get_float_value(self.get_x())

    @Helpers.save_parameter("y")
    def get_y(self):
        return self.get_child_value("y")

    def get_y_value(self):
        return self.get_float_value(self.get_y())
