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

import Helpers
import NSObject
import CGRect


class UIScreen_SynthProvider(NSObject.NSObject_SynthProvider):
    def __init__(self, value_obj, internal_dict):
        super(UIScreen_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIScreen"

        self.bounds = None
        self.scale = None
        self.horizontal_scale = None
        self.interface_idiom = None

    @Helpers.save_parameter("bounds")
    def get_bounds(self):
        return self.get_child_value("_bounds")

    def get_bounds_provider(self):
        bounds = self.get_bounds()
        return None if bounds is None else CGRect.CGRect_SynthProvider(bounds, self.internal_dict)

    def get_bounds_summary(self):
        w = self.get_bounds_provider().get_size_provider().get_width_value()
        h = self.get_bounds_provider().get_size_provider().get_height_value()
        return "size=({}, {})".format(self.formatted_float(w), self.formatted_float(h))

    @Helpers.save_parameter("scale")
    def get_scale(self):
        return self.get_child_value("_scale")

    def get_scale_value(self):
        return self.get_float_value(self.get_scale())

    def get_scale_summary(self):
        scale_value = self.get_scale_value()
        return None if scale_value is None else "scale={}".format(self.formatted_float(scale_value))

    @Helpers.save_parameter("horizontal_scale")
    def get_horizontal_scale(self):
        return self.get_child_value("_horizontalScale")

    def get_horizontal_scale_value(self):
        return self.get_float_value(self.get_horizontal_scale())

    def get_horizontal_scale_summary(self):
        horizontal_scale_value = self.get_horizontal_scale_value()
        return None if horizontal_scale_value is None else "hScale={:.0f}".format(self.formatted_float(horizontal_scale_value))

    @Helpers.save_parameter("interface_idiom")
    def get_interface_idiom(self):
        return self.get_child_value("_userInterfaceIdiom")

    def get_interface_idiom_value(self):
        interface_idiom_value = self.get_interface_idiom().GetValueAsSigned()
        interface_idiom_name = "Unknown"
        if interface_idiom_value == 0:
            interface_idiom_name = "Phone"
        elif interface_idiom_value == 1:
            interface_idiom_name = "Pad"
        return interface_idiom_name

    def get_interface_idiom_summary(self):
        interface_idiom_name = self.get_interface_idiom_value()
        return None if interface_idiom_name is None else "idiom={}".format(interface_idiom_name)

    def summary(self):
        bounds_summary = self.get_bounds_summary()
        scale_summary = self.get_scale_summary()
        # horizontal_scale_summary = self.get_horizontal_scale_summary()
        interface_idiom_summary = self.get_interface_idiom_summary()

        # Summaries
        summaries = [bounds_summary, scale_summary, interface_idiom_summary]
        summary = ", ".join(summaries)
        return summary


def UIScreen_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIScreen_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIScreen.UIScreen_SummaryProvider \
                            --category UIKit \
                            UIScreen")
    debugger.HandleCommand("type category enable UIKit")
