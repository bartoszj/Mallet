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

from ...scripts import helpers
from .. import SummaryBase
import UIControl


class UISliderSyntheticProvider(UIControl.UIControlSyntheticProvider):
    """
    Class representing UISlider.
    """
    def __init__(self, value_obj, internal_dict):
        super(UISliderSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UISlider"

        self.register_child_value("value", "_value", primitive_value_function=SummaryBase.get_float_value, summary_function=self.get_value_summary)
        self.register_child_value("min", "_minValue", primitive_value_function=SummaryBase.get_float_value, summary_function=self.get_min_summary)
        self.register_child_value("max", "_maxValue", primitive_value_function=SummaryBase.get_float_value, summary_function=self.get_max_summary)

    @staticmethod
    def get_value_summary(value):
        return "value={}".format(SummaryBase.formatted_float(value))

    @staticmethod
    def get_min_summary(value):
        return "min={}".format(SummaryBase.formatted_float(value))

    @staticmethod
    def get_max_summary(value):
        return "max={}".format(SummaryBase.formatted_float(value))

    def summary(self):
        summary = SummaryBase.join_summaries(self.value_summary, self.min_summary, self.max_summary)
        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UISliderSyntheticProvider)
