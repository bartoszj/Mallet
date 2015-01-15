#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Bartosz Janda
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
import UIColor


class UIDeviceRGBColorSyntheticProvider(UIColor.UIColorSyntheticProvider):
    """
    Class representing UIDeviceRGBColor.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIDeviceRGBColorSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIDeviceRGBColor"

        self.register_child_value("red_component", ivar_name="redComponent",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_red_component_summary)
        self.register_child_value("green_component", ivar_name="greenComponent",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_green_component_summary)
        self.register_child_value("blue_component", ivar_name="blueComponent",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_blue_component_summary)
        self.register_child_value("alpha_component", ivar_name="alphaComponent",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_alpha_component_summary)

    @staticmethod
    def get_red_component_summary(value):
        return "red={}".format(SummaryBase.formatted_float(value))

    @staticmethod
    def get_green_component_summary(value):
        return "green={}".format(SummaryBase.formatted_float(value))

    @staticmethod
    def get_blue_component_summary(value):
        return "blue={}".format(SummaryBase.formatted_float(value))

    @staticmethod
    def get_alpha_component_summary(value):
        return "alpha={}".format(SummaryBase.formatted_float(value))

    def summary(self):
        summary = SummaryBase.join_summaries(self.red_component_summary,
                                             self.green_component_summary,
                                             self.blue_component_summary,
                                             self.alpha_component_summary)
        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UIDeviceRGBColorSyntheticProvider)


def lldb_init(debugger, dictionary):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                            --category UIKit \
                            UIDeviceRGBColor UICachedDeviceRGBColor".format(__name__))
    debugger.HandleCommand("type category enable UIKit")
