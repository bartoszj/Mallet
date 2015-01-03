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

import Helpers
import NSObject
import CALayerIvars


class CALayer_SynthProvider(NSObject.NSObjectSyntheticProvider):
    def __init__(self, value_obj, internal_dict):
        super(CALayer_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "CALayer"

        self.attr = None
        self.attr_provider = None

    @Helpers.save_parameter("attr")
    def get_attr(self):
        return self.get_child_value("_attr")

    @Helpers.save_parameter("attr_provider")
    def get_attr_provider(self):
        attr = self.get_attr()
        return None if attr is None else CALayerIvars.CALayerIvars_SynthProvider(attr, self.internal_dict)

    def get_position(self):
        return self.get_attr_provider().get_layer_provider().get_position()

    def get_position_provider(self):
        return self.get_attr_provider().get_layer_provider().get_position_provider()

    def get_position_summary(self):
        position = self.get_position_provider()
        return None if position is None else "position=({}, {})".format(self.formatted_float(position.get_x_value()),
                                                                        self.formatted_float(position.get_y_value()))

    def get_bounds(self):
        return self.get_attr_provider().get_layer_provider().get_bounds()

    def get_bounds_provider(self):
        return self.get_attr_provider().get_layer_provider().get_bounds_provider()

    def get_bounds_summary(self):
        bounds = self.get_bounds_provider()
        return None if bounds is None else "bounds=({} {}; {} {})".format(self.formatted_float(bounds.get_origin_provider().get_x_value()),
                                                                          self.formatted_float(bounds.get_origin_provider().get_y_value()),
                                                                          self.formatted_float(bounds.get_size_provider().get_width_value()),
                                                                          self.formatted_float(bounds.get_size_provider().get_height_value()))

    def summary(self):
        position_summary = self.get_position_summary()
        bounds_summary = self.get_bounds_summary()

        summaries = [position_summary, bounds_summary]
        summary = ", ".join(summaries)

        return summary


def CALayer_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, CALayer_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F CALayer.CALayer_SummaryProvider \
                            --category QuartzCore \
                            CALayer")
    debugger.HandleCommand("type category enable QuartzCore")
