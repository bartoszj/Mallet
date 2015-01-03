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
import SummaryBase
import CALayerIvars


class CALayerSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing CALayer.
    """
    def __init__(self, value_obj, internal_dict):
        super(CALayerSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "CALayer"

        self.register_child_value("attr", ivar_name="_attr", provider_class=CALayerIvars.CALayerIvarsSyntheticProvider)

    def get_position_provider(self):
        """
        Returns position provider.

        :return: Position provider.
        :rtype: CADoublePoint.CADoublePointSyntheticProvider
        """
        return self.attr_provider.layer_provider.position_provider

    def get_position_summary(self):
        """
        Returns position summary.

        :return: Position summary.
        :rtype: str
        """
        position = self.get_position_provider()
        return None if position is None else "position=({}, {})".format(SummaryBase.formatted_float(position.x_value),
                                                                        SummaryBase.formatted_float(position.y_value))

    def get_bounds_provider(self):
        """
        Returns bounds provider.

        :return: bounds provider.
        :rtype: CADoubleRect.CADoubleRectSyntheticProvider
        """
        return self.attr_provider.layer_provider.bounds_provider

    def get_bounds_summary(self):
        """
        Returns bounds summary.
        :return: Bounds summary.
        :rtype: str
        """
        bounds = self.get_bounds_provider()
        return None if bounds is None else "bounds=({} {}; {} {})".format(SummaryBase.formatted_float(bounds.origin_provider.x_value),
                                                                          SummaryBase.formatted_float(bounds.origin_provider.y_value),
                                                                          SummaryBase.formatted_float(bounds.size_provider.width_value),
                                                                          SummaryBase.formatted_float(bounds.size_provider.height_value))

    def summary(self):
        summary = SummaryBase.join_summaries(self.get_position_summary(), self.get_bounds_summary())
        return summary


def summary_provider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, CALayerSyntheticProvider)


def __lldb_init_module(debugger, dictionary):
    debugger.HandleCommand("type summary add -F CALayer.summary_provider \
                            --category QuartzCore \
                            CALayer")
    debugger.HandleCommand("type category enable QuartzCore")
