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

from ...scripts import helpers
from .. import SummaryBase
import UIControl


class UISegmentedControlSyntheticProvider(UIControl.UIControlSyntheticProvider):
    def __init__(self, value_obj, internal_dict):
        super(UISegmentedControlSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UISegmentedControl"

        self.register_child_value("segments", ivar_name="_segments",
                                  primitive_value_function=SummaryBase.get_count_value,
                                  summary_function=self.get_segments_summary)
        self.register_child_value("selected_segment", ivar_name="_selectedSegment",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_selected_segments_summary)
        self.register_child_value("highlighted_segment", ivar_name="_highlightedSegment",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_highlighted_segment_summary)

    @staticmethod
    def get_segments_summary(value):
        return "segments={}".format(value)

    @staticmethod
    def get_selected_segments_summary(value):
        return "selected={}".format(value)

    @staticmethod
    def get_highlighted_segment_summary(value):
        return "highlighted={}".format(value)

    def summary(self):
        summary = SummaryBase.join_summaries(self.selected_segment_summary, self.segments_summary)
        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UISegmentedControlSyntheticProvider)


def __lldb_init_module(debugger, dictionary):
    debugger.HandleCommand("type summary add -F UISegmentedControl.summary_provider \
                            --category UIKit \
                            UISegmentedControl")
    debugger.HandleCommand("type category enable UIKit")
