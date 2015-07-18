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

from .. import helpers
from ..common import SummaryBase
import UIView


UIActivityIndicatorViewStyleWhiteLarge = 0
UIActivityIndicatorViewStyleWhite = 1
UIActivityIndicatorViewStyleGray = 2


class UIActivityIndicatorViewSyntheticProvider(UIView.UIViewSyntheticProvider):
    """
    Class representing UIActivityIndicatorView.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIActivityIndicatorViewSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIActivityIndicatorView"

        self.register_child_value("duration", ivar_name="_duration",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_duration_summary)
        self.register_child_value("animating", ivar_name="_animating",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_animating_summary)
        self.register_child_value("activity_indicator_view_style", ivar_name="_activityIndicatorViewStyle",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_activity_indicator_view_style_summary)
        self.register_child_value("hides_when_stopped", ivar_name="_hidesWhenStopped",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_hides_when_stopped_summary)

    @staticmethod
    def get_duration_summary(value):
        return "duration={}".format(SummaryBase.formatted_float(value))

    @staticmethod
    def get_animating_summary(value):
        if value:
            return "animating"
        return None

    @staticmethod
    def get_activity_indicator_view_style_summary(value):
        style = get_activity_indicator_style_text(value)
        return "style={}".format(style)

    @staticmethod
    def get_hides_when_stopped_summary(value):
        if value:
            return "hidesWhenStopped"
        return None

    def summaries_parts(self):
        return [self.animating_summary,
                self.hides_when_stopped_summary,
                self.activity_indicator_view_style_summary]


def get_activity_indicator_style_text(value):
    if value == UIActivityIndicatorViewStyleWhiteLarge:
        return "WhiteLarge"
    elif value == UIActivityIndicatorViewStyleWhite:
        return "White"
    elif value == UIActivityIndicatorViewStyleGray:
        return "Gray"
    return "Unknown"


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UIActivityIndicatorViewSyntheticProvider)
