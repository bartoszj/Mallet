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
import Helpers


class CADoubleRect_SynthProvider(SummaryBase.SummaryBaseSyntheticProvider):
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

    @Helpers.save_parameter("origin")
    def get_origin(self):
        # Using CGPoint for workaround. LLDB cannot find type CADoublePoint.
        return self.get_child_value("origin", type_name="CGPoint", offset=0)

    @Helpers.save_parameter("origin_provider")
    def get_origin_provider(self):
        origin = self.get_origin()
        return None if origin is None else CADoublePoint.CADoublePoint_SynthProvider(origin, self.internal_dict)

    def get_origin_summary(self):
        origin = self.get_origin_provider()
        return None if origin is None else "origin={}".format(origin.summary())

    @Helpers.save_parameter("size")
    def get_size(self):
        # Using CGSize for workaround. LLDB cannot find type CADoubleSize.
        return self.get_child_value("size", type_name="CGSize", offset=16)

    @Helpers.save_parameter("size_provider")
    def get_size_provider(self):
        size = self.get_size()
        return None if size is None else CADoubleSize.CADoubleSize_SynthProvider(size, self.internal_dict)

    def get_size_summary(self):
        size = self.get_size_provider()
        return None if size is None else "size={}".format(size.summary())

    def summary(self):
        origin_summary = self.get_origin_summary()
        size_summary = self.get_size_summary()

        summaries = [origin_summary, size_summary]
        summary = ", ".join(summaries)
        return summary
