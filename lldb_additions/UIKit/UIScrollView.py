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

from ...scripts import helpers
from .. import SummaryBase
from ..CoreGraphics import CGSize
import UIView
import UIEdgeInsets


class UIScrollViewSyntheticProvider(UIView.UIViewSyntheticProvider):
    """
    Class representing UIScrollView.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIScrollViewSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIScrollView"

        self.register_child_value("content_size", ivar_name="_contentSize",
                                  provider_class=CGSize.CGSizeSyntheticProvider,
                                  summary_function=self.get_content_size_summary)
        self.register_child_value("content_inset", ivar_name="_contentInset",
                                  provider_class=UIEdgeInsets.UIEdgeInsetsSyntheticProvider,
                                  summary_function=self.get_content_inset_summary)
        self.register_child_value("minimum_zoom_scale", ivar_name="_minimumZoomScale",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_minimum_zoom_scale_summary)
        self.register_child_value("maximum_zoom_scale", ivar_name="_maximumZoomScale",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_maximum_zoom_scale_summary)

    def get_content_offset_summary(self):
        origin = self.layer_provider.get_bounds_provider().origin_provider
        return "contentOffset=({}, {})".format(SummaryBase.formatted_float(origin.x_value),
                                               SummaryBase.formatted_float(origin.y_value))

    @staticmethod
    def get_content_size_summary(provider):
        return "contentSize=({}, {})".format(SummaryBase.formatted_float(provider.width_value),
                                             SummaryBase.formatted_float(provider.height_value))

    @staticmethod
    def get_content_inset_summary(provider):
        if provider.top_value != 0 and provider.left_value != 0 and provider.bottom_value != 0 and provider.right_value != 0:
            return "inset=({}, {}, {}, {})".format(SummaryBase.formatted_float(provider.top_value),
                                                   SummaryBase.formatted_float(provider.left_value),
                                                   SummaryBase.formatted_float(provider.bottom_value),
                                                   SummaryBase.formatted_float(provider.right_value))
        return None

    @staticmethod
    def get_minimum_zoom_scale_summary(value):
        if value != 1:
            return "minScale={}".format(SummaryBase.formatted_float(value))
        return None

    @staticmethod
    def get_maximum_zoom_scale_summary(value):
        if value != 1:
            return "maxScale={}".format(SummaryBase.formatted_float(value))
        return None

    def summaries_parts(self):
        return [self.get_frame_summary(),
                self.get_content_offset_summary(),
                self.content_size_summary,
                self.content_inset_summary,
                self.minimum_zoom_scale_summary,
                self.maximum_zoom_scale_summary,
                self.tag_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UIScrollViewSyntheticProvider)
