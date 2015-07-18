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

from .. import helpers
from ..common import SummaryBase
from ..Foundation import NSObject
from ..CoreGraphics import CGRect


class UIScreenSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing UIScreen.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIScreenSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIScreen"

        self.register_child_value("bounds", ivar_name="_bounds",
                                  provider_class=CGRect.CGRectSyntheticProvider,
                                  summary_function=self.get_bounds_summary)
        self.register_child_value("scale", ivar_name="_scale",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_scale_summary)
        self.register_child_value("horizontal_scale", ivar_name="_horizontalScale",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_horizontal_scale_summary)
        self.register_child_value("interface_idiom", ivar_name="_userInterfaceIdiom",
                                  primitive_value_function=self.get_interface_idiom_value,
                                  summary_function=self.get_interface_idiom_summary)

    @staticmethod
    def get_bounds_summary(provider):
        return "size=({}, {})".format(SummaryBase.formatted_float(provider.size_provider.width_value),
                                      SummaryBase.formatted_float(provider.size_provider.height_value))

    @staticmethod
    def get_scale_summary(value):
        return "scale={}".format(SummaryBase.formatted_float(value))

    @staticmethod
    def get_horizontal_scale_summary(value):
        return "hScale={:.0f}".format(SummaryBase.formatted_float(value))

    @staticmethod
    def get_interface_idiom_value(value):
        interface_idiom_value = value.GetValueAsSigned()
        interface_idiom_name = "Unknown"
        if interface_idiom_value == 0:
            interface_idiom_name = "Phone"
        elif interface_idiom_value == 1:
            interface_idiom_name = "Pad"
        return interface_idiom_name

    @staticmethod
    def get_interface_idiom_summary(value):
        return "idiom={}".format(value)

    def summaries_parts(self):
        return [self.bounds_summary, self.scale_summary, self.interface_idiom_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UIScreenSyntheticProvider)
