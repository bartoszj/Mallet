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


class CADoubleRectSyntheticProvider(SummaryBase.SummaryBaseSyntheticProvider):
    """
    Class representing CADoubleRect structure.
    """
    # struct CADoubleRect {
    #     struct CADoublePoint origin;
    #     struct CADoubleSize size;
    # };
    def __init__(self, value_obj, internal_dict):
        super(CADoubleRectSyntheticProvider, self).__init__(value_obj, internal_dict)

        # Using CGPoint for workaround. LLDB cannot find type CADoublePoint.
        self.register_child_value("origin", ivar_name="origin", type_name="CGPoint", offset=0,
                                  provider_class=CADoublePoint.CADoublePointSyntheticProvider,
                                  summary_function=self.get_origin_summary)
        # Using CGSize for workaround. LLDB cannot find type CADoubleSize.
        self.register_child_value("size", ivar_name="size", type_name="CGSize", offset=16,
                                  provider_class=CADoubleSize.CADoubleSizeSyntheticProvider,
                                  summary_function=self.get_size_summary)

    @staticmethod
    def get_origin_summary(provider):
        """
        :param CADoublePoint.CADoublePointSyntheticProvider provider: CADoublePoint provider.
        """
        return "origin={}".format(provider.summary())

    @staticmethod
    def get_size_summary(provider):
        """
        :param CADoubleSize.CADoubleSizeSyntheticProvider provider: CADoublePoint provider.
        """
        return "size={}".format(provider.summary())

    def summary(self):
        summary = SummaryBase.join_summaries(self.origin_summary, self.size_summary)
        return summary
