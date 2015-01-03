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


class UIView_SynthProvider(UIResponder.UIResponder_SynthProvider):
    def __init__(self, value_obj, internal_dict):
        super(UIView_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIView"

        self.frame = None
        self.tag = None
        self.layer = None
        self.layer_provider = None

    @Helpers.save_parameter("frame")
    def get_frame(self):
        if not self.has_valid_layer():
            return None

        position = self.get_layer_provider().get_position_provider()
        bounds = self.get_layer_provider().get_bounds_provider()

        frame = Rect()
        frame.width = bounds.get_size_provider().get_width_value()
        frame.height = bounds.get_size_provider().get_height_value()
        frame.x = position.get_x_value() - frame.width / 2
        frame.y = position.get_y_value() - frame.height / 2
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

    @Helpers.save_parameter("tag")
    def get_tag(self):
        return self.get_child_value("_tag")

    def get_tag_value(self):
        return SummaryBase.get_signed_value(self.get_tag())

    def get_tag_summary(self):
        return "tag={}".format(self.get_tag_value())

    @Helpers.save_parameter("layer")
    def get_layer(self):
        return self.get_child_value("_layer")

    def has_valid_layer(self):
        # In some cases CALayer object is invalid.
        layer = self.get_layer()
        class_data, wrapper = Helpers.get_class_data(layer)
        if class_data.is_valid() is None:
            logger = logging.getLogger(__name__)
            logger.info("has_valid_layer: not valid class_data.")
            return False
        return True

    @Helpers.save_parameter("layer_provider")
    def get_layer_provider(self):
        layer = self.get_layer()
        return None if layer is None else CALayer.CALayer_SynthProvider(layer, self.internal_dict)

    def summary(self):
        frame_summary = self.get_frame_summary()
        tag_summary = self.get_tag_summary()

        summaries = []
        if frame_summary:
            summaries.append(frame_summary)
        if self.get_tag_value() != 0:
            summaries.append(tag_summary)

        summary = ", ".join(summaries)
        return summary


def UIView_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIView_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIView.UIView_SummaryProvider \
                            --category UIKit \
                            UIImageView UIView UIWindow")
    debugger.HandleCommand("type category enable UIKit")
