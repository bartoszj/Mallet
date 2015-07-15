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

from ..common import SummaryBase


class CADoubleSizeSyntheticProvider(SummaryBase.SummaryBaseSyntheticProvider):
    """
    Class representing CADoubleSize structure.
    """
    # struct CADoubleSize {
    #     double width;
    #     double height;
    # };
    def __init__(self, value_obj, internal_dict):
        super(CADoubleSizeSyntheticProvider, self).__init__(value_obj, internal_dict)

        self.register_child_value("width", ivar_name="width", type_name="double", offset=0,
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_width_summary)
        self.register_child_value("height", ivar_name="height", type_name="double", offset=8,
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_height_summary)

    @staticmethod
    def get_width_summary(value):
        return "width={}".format(SummaryBase.formatted_float(value))

    @staticmethod
    def get_height_summary(value):
        return "height={}".format(SummaryBase.formatted_float(value))

    def summary(self):
        summary = "(width={}, height={})".format(self.width_summary, self.height_summary)
        return summary
