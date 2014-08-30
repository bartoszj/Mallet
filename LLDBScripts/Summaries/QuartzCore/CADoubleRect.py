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
import CADoublePoint
import CADoubleSize


class CADoubleRect_SynthProvider(SummaryBase.SummaryBase_SynthProvider):
    # struct CADoubleRect {
    #     struct CADoublePoint origin;
    #     struct CADoubleSize size;
    # };
    def __init__(self, value_obj, internal_dict):
        super(CADoubleRect_SynthProvider, self).__init__(value_obj, internal_dict)

        self.origin = None
        self.size = None

        self.origin_provider = None
        self.size_provider = None

    def get_origin(self):
        if self.origin:
            return self.origin

        # Using CGPoint for workaround. LLDB cannot find type CADoublePoint.
        self.origin = self.get_child_value("origin", type_name="CGPoint", offset=0)
        return self.origin

    def get_origin_provider(self):
        if self.origin_provider:
            return self.origin_provider

        origin = self.get_origin()
        self.origin_provider = CADoublePoint.CADoublePoint_SynthProvider(origin, self.internal_dict)
        return self.origin_provider

    def get_size(self):
        if self.size:
            return self.size

        # Using CGSize for workaround. LLDB cannot find type CADoubleSize.
        self.size = self.get_child_value("size", type_name="CGSize", offset=16)
        return self.size

    def get_size_provider(self):
        if self.size_provider:
            return self.size_provider

        size = self.get_size()
        self.size_provider = CADoubleSize.CADoubleSize_SynthProvider(size, self.internal_dict)
        return self.size_provider

    def summary(self):
        o = self.get_origin_provider()
        s = self.get_size_provider()
        summary = "origin={}, size={}".format(o.summary(), s.summary())
        return summary
