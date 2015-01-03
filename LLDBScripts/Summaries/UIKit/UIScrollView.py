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
import SummaryBase
import UIView
import CGSize
import UIEdgeInsets


class UIScrollView_SynthProvider(UIView.UIView_SynthProvider):
    def __init__(self, value_obj, internal_dict):
        super(UIScrollView_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIScrollView"

        self.content_size = None
        self.content_inset = None
        self.minimum_zoom_scale = None
        self.maximum_zoom_scale = None

    def get_content_offset_summary(self):
        if self.has_valid_layer() is None:
            return None
        origin = self.get_layer_provider().get_bounds_provider().get_origin_provider()
        return "contentOffset=({}, {})".format(SummaryBase.formatted_float(origin.get_x_value()),
                                               SummaryBase.formatted_float(origin.get_y_value()))

    @Helpers.save_parameter("content_size")
    def get_content_size(self):
        return self.get_child_value("_contentSize")

    def get_content_size_provider(self):
        content_size = self.get_content_size()
        return None if content_size is None else CGSize.CGSize_SynthProvider(content_size, self.internal_dict)

    def get_content_size_summary(self):
        content_size_w = self.get_content_size_provider().get_width_value()
        content_size_h = self.get_content_size_provider().get_height_value()
        return "contentSize=({}, {})".format(SummaryBase.formatted_float(content_size_w), SummaryBase.formatted_float(content_size_h))

    @Helpers.save_parameter("content_inset")
    def get_content_inset(self):
        return self.get_child_value("_contentInset")

    def get_content_inset_provider(self):
        content_inset = self.get_content_inset()
        return None if content_inset is None else UIEdgeInsets.UIEdgeInsets_SynthProvider(content_inset, self.internal_dict)

    def get_content_inset_summary(self):
        content_inset_t = self.get_content_inset_provider().get_top_value()
        content_inset_l = self.get_content_inset_provider().get_left_value()
        content_inset_b = self.get_content_inset_provider().get_bottom_value()
        content_inset_r = self.get_content_inset_provider().get_right_value()
        return "inset=({}, {}, {}, {})".format(SummaryBase.formatted_float(content_inset_t),
                                               SummaryBase.formatted_float(content_inset_l),
                                               SummaryBase.formatted_float(content_inset_b),
                                               SummaryBase.formatted_float(content_inset_r))

    @Helpers.save_parameter("minimum_zoom_scale")
    def get_minimum_zoom_scale(self):
        return self.get_child_value("_minimumZoomScale")

    def get_minimum_zoom_scale_value(self):
        return SummaryBase.get_float_value(self.get_minimum_zoom_scale())

    def get_minimum_zoom_scale_summary(self):
        minimum_zoom_scale_value = self.get_minimum_zoom_scale_value()
        return None if minimum_zoom_scale_value is None else "minScale={}".format(SummaryBase.formatted_float(minimum_zoom_scale_value))

    @Helpers.save_parameter("maximum_zoom_scale")
    def get_maximum_zoom_scale(self):
        return self.get_child_value("_maximumZoomScale")

    def get_maximum_zoom_scale_value(self):
        return SummaryBase.get_float_value(self.get_maximum_zoom_scale())

    def get_maximum_zoom_scale_summary(self):
        maximum_zoom_scale_value = self.get_maximum_zoom_scale_value()
        return None if maximum_zoom_scale_value is None else "maxScale={}".format(SummaryBase.formatted_float(maximum_zoom_scale_value))

    def summary(self):
        frame_summary = self.get_frame_summary()
        content_offset_summary = self.get_content_offset_summary()
        content_size_summary = self.get_content_size_summary()

        content_inset_t = self.get_content_inset_provider().get_top_value()
        content_inset_l = self.get_content_inset_provider().get_left_value()
        content_inset_b = self.get_content_inset_provider().get_bottom_value()
        content_inset_r = self.get_content_inset_provider().get_right_value()
        content_inset_summary = self.get_content_inset_summary()

        minimum_zoom_scale_value = self.get_minimum_zoom_scale_value()
        minimum_zoom_scale_summary = self.get_minimum_zoom_scale_summary()

        maximum_zoom_scale_value = self.get_maximum_zoom_scale_value()
        maximum_zoom_scale_summary = self.get_maximum_zoom_scale_summary()
        tag_summary = self.get_tag_summary()

        # Summaries
        summaries = []
        if frame_summary:
            summaries.append(frame_summary)
        if content_offset_summary:
            summaries.append(content_offset_summary)
        if content_size_summary:
            summaries.append(content_size_summary)
        if content_inset_t != 0 or content_inset_l != 0 or content_inset_b != 0 or content_inset_r != 0:
            summaries.append(content_inset_summary)
        if minimum_zoom_scale_value != 1:
            summaries.append(minimum_zoom_scale_summary)
        if maximum_zoom_scale_value != 1:
            summaries.append(maximum_zoom_scale_summary)
        if self.get_tag_value() != 0:
            summaries.append(tag_summary)

        summary = ", ".join(summaries)
        return summary


def UIScrollView_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIScrollView_SynthProvider)


def __lldb_init_module(debugger, dictionary):
    debugger.HandleCommand("type summary add -F UIScrollView.UIScrollView_SummaryProvider \
                            --category UIKit \
                            UIScrollView")
    debugger.HandleCommand("type category enable UIKit")
