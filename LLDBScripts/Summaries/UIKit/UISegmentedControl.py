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
import SummaryBase
import UIControl


class UISegmentedControl_SynthProvider(UIControl.UIControl_SynthProvider):
    def __init__(self, value_obj, internal_dict):
        super(UISegmentedControl_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UISegmentedControl"

        self.segments = None
        self.selected_segment = None
        self.highlighted_segment = None

    @Helpers.save_parameter("segments")
    def get_segments(self):
        return self.get_child_value("_segments")

    def get_segments_value(self):
        return SummaryBase.get_count_value(self.get_segments())

    def get_segments_summary(self):
        segments_value = self.get_segments_value()
        return None if segments_value is None else "segments={}".format(segments_value)

    @Helpers.save_parameter("selected_segment")
    def get_selected_segments(self):
        return self.get_child_value("_selectedSegment")

    def get_selected_segments_value(self):
        return SummaryBase.get_signed_value(self.get_selected_segments())

    def get_selected_segments_summary(self):
        selected_segments_value = self.get_selected_segments_value()
        return None if selected_segments_value is None else "selected={}".format(selected_segments_value)

    @Helpers.save_parameter("highlighted_segment")
    def get_highlighted_segment(self):
        return self.get_child_value("_highlightedSegment")

    def get_highlighted_segment_value(self):
        return SummaryBase.get_signed_value(self.get_highlighted_segment())

    def get_highlighted_segment_summary(self):
        highlighted_segment_value = self.get_highlighted_segment_value()
        return None if highlighted_segment_value is None else "highlighted={}".format(highlighted_segment_value)

    def summary(self):
        segments_summary = self.get_segments_summary()
        selected_segment_summary = self.get_selected_segments_summary()
        # highlighted_segment_summary = self.get_highlighted_segment_summary()

        # Summaries
        summaries = [selected_segment_summary, segments_summary]

        summary = ", ".join(summaries)
        return summary


def UISegmentedControl_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UISegmentedControl_SynthProvider)


def __lldb_init_module(debugger, dictionary):
    debugger.HandleCommand("type summary add -F UISegmentedControl.UISegmentedControl_SummaryProvider \
                            --category UIKit \
                            UISegmentedControl")
    debugger.HandleCommand("type category enable UIKit")
