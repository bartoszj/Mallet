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
import UIControl


class UISegmentedControl_SynthProvider(UIControl.UIControl_SynthProvider):
    # Class: UISegmentedControl
    # Super class: UIControl
    # Protocols: _UIBasicAnimationFactory, NSCoding
    # Name:                                                                     armv7                 i386                  arm64                 x86_64
    # NSMutableArray * _segments                                            120 (0x078) / 4       120 (0x078) / 4       224 (0x0E0) / 8       224 (0x0E0) / 8
    # NSInteger _selectedSegment                                            124 (0x07C) / 4       124 (0x07C) / 4       232 (0x0E8) / 8       232 (0x0E8) / 8
    # NSInteger _highlightedSegment                                         128 (0x080) / 4       128 (0x080) / 4       240 (0x0F0) / 8       240 (0x0F0) / 8
    # UIView * _removedSegment                                              132 (0x084) / 4       132 (0x084) / 4       248 (0x0F8) / 8       248 (0x0F8) / 8
    # NSInteger _barStyle                                                   136 (0x088) / 4       136 (0x088) / 4       256 (0x100) / 8       256 (0x100) / 8
    # id _appearanceStorage                                                 140 (0x08C) / 4       140 (0x08C) / 4       264 (0x108) / 8       264 (0x108) / 8
    # UIView * _backgroundBarView                                           144 (0x090) / 4       144 (0x090) / 4       272 (0x110) / 8       272 (0x110) / 8
    # CGFloat _enabledAlpha                                                 148 (0x094) / 4       148 (0x094) / 4       280 (0x118) / 8       280 (0x118) / 8
    # struct {
    #         unsigned int style:3;
    #         unsigned int size:2;
    #         unsigned int delegateAlwaysNotifiesDelegateOfSegmentClicks:1;
    #         unsigned int momentaryClick:1;
    #         unsigned int tracking:1;
    #         unsigned int autosizeToFitSegments:1;
    #         unsigned int isSizingToFit:1;
    #         unsigned int autosizeText:1;
    #         unsigned int transparentBackground:1;
    #         unsigned int useProportionalWidthSegments:1;
    #         unsigned int translucentBackground:1;
    #         unsigned int appearanceNeedsUpdate:1;
    #         unsigned int contentTextPaddingEnabled:1;
    #     } _segmentedControlFlags                                          152 (0x098) / 2       152 (0x098) / 4       288 (0x120) / 4       288 (0x120) / 4
    # BOOL __hasTranslucentOptionsBackground                                154 (0x09A) / 1       156 (0x09C) / 1       292 (0x124) / 1       292 (0x124) / 1

    def __init__(self, value_obj, internal_dict):
        super(UISegmentedControl_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UISegmentedControl"

        self.segments = None
        self.selected_segment = None
        self.highlighted_segment = None

    def get_segments(self):
        if self.segments:
            return self.segments

        self.segments = self.get_child_value("_segments")
        return self.segments

    def get_selected_segments(self):
        if self.selected_segment:
            return self.selected_segment

        self.selected_segment = self.get_child_value("_selectedSegment")
        return self.selected_segment

    def get_highlighted_segment(self):
        if self.highlighted_segment:
            return self.highlighted_segment

        self.highlighted_segment = self.get_child_value("_highlightedSegment")
        return self.highlighted_segment

    def summary(self):
        segments = self.get_segments()
        segments_value = segments.GetNumChildren()
        segments_summary = "segments={}".format(segments_value)

        selected_segment = self.get_selected_segments()
        selected_segment_value = selected_segment.GetValueAsSigned()
        selected_segment_summary = "selected={}".format(selected_segment_value)

        # highlighted_segment = self.get_highlighted_segment()
        # highlighted_segment_value = highlighted_segment.GetValueAsSigned()
        # highlighted_segment_summary = "highlighted={}".format(highlighted_segment_value)

        # Summaries
        summaries = [selected_segment_summary, segments_summary]

        summary = ", ".join(summaries)
        return summary


def UISegmentedControl_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UISegmentedControl_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UISegmentedControl.UISegmentedControl_SummaryProvider \
                            --category UIKit \
                            UISegmentedControl")
    debugger.HandleCommand("type category enable UIKit")
