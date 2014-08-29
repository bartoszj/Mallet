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


class CGVector_SynthProvider(SummaryBase.SummaryBase_SynthProvider):
    # struct CGVector {
    #   CGFloat dx;
    #   CGFloat dy;
    # };
    # typedef struct CGVector CGVector;
    def __init__(self, value_obj, internal_dict):
        super(CGVector_SynthProvider, self).__init__(value_obj, internal_dict)

        self.dx = None
        self.dy = None

    def get_dx(self):
        if self.dx:
            return self.dx

        self.dx = self.get_child_value("dx")
        return self.dx

    def get_dx_value(self):
        dx = self.get_dx()
        return float(dx.GetValue())

    def get_dy(self):
        if self.dy:
            return self.dy

        self.dy = self.get_child_value("dy")
        return self.dy

    def get_dy_value(self):
        dy = self.get_dy()
        return float(dy.GetValue())
