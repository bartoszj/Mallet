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


class CADoubleSize_SynthProvider(SummaryBase.SummaryBaseSyntheticProvider):
    # struct CADoubleSize {
    #     double width;
    #     double height;
    # };
    def __init__(self, value_obj, internal_dict):
        super(CADoubleSize_SynthProvider, self).__init__(value_obj, internal_dict)

        self.width = None
        self.height = None

    @Helpers.save_parameter("width")
    def get_width(self):
        return self.get_child_value("width", type_name="double", offset=0)

    def get_width_value(self):
        return SummaryBase.get_float_value(self.get_width())

    def get_width_summary(self):
        width = self.get_width_value()
        return None if width is None else "width={}".format(SummaryBase.formatted_float(width))

    @Helpers.save_parameter("height")
    def get_height(self):
        return self.get_child_value("height", type_name="double", offset=8)

    def get_height_value(self):
        return SummaryBase.get_float_value(self.get_height())

    def get_height_summary(self):
        height = self.get_height_value()
        return None if height is None else "height={}".format((SummaryBase.formatted_float(height)))

    def summary(self):
        summary = "(width={}, height={})".format(self.get_width_summary(), self.get_height_summary())
        return summary
