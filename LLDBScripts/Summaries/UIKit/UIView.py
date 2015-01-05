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

import logging
import Helpers
import SummaryBase
import UIResponder
import CALayer


class Rect(object):
    def __init__(self):
        self.x = None
        self.y = None
        self.width = None
        self.height = None


class UIViewSyntheticProvider(UIResponder.UIResponderSyntheticProvider):
    """
    Class representing UIView.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIViewSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIView"

        self.register_child_value("tag", ivar_name="_tag",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_tag_summary)
        self.register_child_value("layer", ivar_name="_layer",
                                  provider_class=CALayer.CALayerSyntheticProvider)
        self.frame = None

    @staticmethod
    def get_tag_summary(value):
        if value != 0:
            return "tag={}".format(value)
        else:
            return None

    @Helpers.save_parameter("frame")
    def get_frame(self):
        position = self.layer_provider.get_position_provider()
        bounds = self.layer_provider.get_bounds_provider()

        frame = Rect()
        frame.width = bounds.size_provider.width_value
        frame.height = bounds.size_provider.height_value
        frame.x = position.x_value - frame.width / 2
        frame.y = position.y_value - frame.height / 2
        return frame

    def get_frame_summary(self):
        frame = self.get_frame()
        if frame is None:
            return None

        frame_summary = "frame=({} {}; {} {})".format(SummaryBase.formatted_float(frame.x),
                                                      SummaryBase.formatted_float(frame.y),
                                                      SummaryBase.formatted_float(frame.width),
                                                      SummaryBase.formatted_float(frame.height))
        return frame_summary

    def summary(self):
        summary = SummaryBase.join_summaries(self.get_frame_summary(), self.tag_summary)
        return summary


def summary_provider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIViewSyntheticProvider)


def __lldb_init_module(debugger, dictionary):
    debugger.HandleCommand("type summary add -F UIView.summary_provider \
                            --category UIKit \
                            UIImageView UIView UIWindow")
    debugger.HandleCommand("type category enable UIKit")
