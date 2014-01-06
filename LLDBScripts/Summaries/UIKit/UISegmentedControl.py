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

import lldb
import summary_helpers
import UIControl


class UISegmentedControl_SynthProvider(UIControl.UIControl_SynthProvider):
    # UISegmentedControl:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSMutableArray *_segments                                             120 = 0x78 / 4          224 = 0xe0 / 8
    # NSInteger _selectedSegment                                            124 = 0x7c / 4          232 = 0xe8 / 8
    # NSInteger _highlightedSegment                                         128 = 0x80 / 4          240 = 0xf0 / 8
    # UIView *_removedSegment                                               132 = 0x84 / 4          248 = 0xf8 / 8
    # NSInteger _barStyle                                                   136 = 0x88 / 4          256 = 0x100 / 8
    # id _appearanceStorage                                                 140 = 0x8c / 4          264 = 0x108 / 8
    # UIView *_backgroundBarView                                            144 = 0x90 / 4          272 = 0x110 / 8
    # CGFloat _enabledAlpha                                                 148 = 0x94 / 4          280 = 0x118 / 8
    # struct {
    #     unsigned int style:3;
    #     unsigned int size:2;
    #     unsigned int delegateAlwaysNotifiesDelegateOfSegmentClicks:1;
    #     unsigned int momentaryClick:1;
    #     unsigned int tracking:1;
    #     unsigned int autosizeToFitSegments:1;
    #     unsigned int isSizingToFit:1;
    #     unsigned int autosizeText:1;
    #     unsigned int transparentBackground:1;
    #     unsigned int useProportionalWidthSegments:1;
    #     unsigned int translucentBackground:1;
    #     unsigned int appearanceNeedsUpdate:1;
    # } _segmentedControlFlags                                              152 = 0x98 / 2 + 2      288 = 0x120 / 2 + 2
    # BOOL __hasTranslucentOptionsBackground                                156 = 0x9c / 1          292 = 0x124 / 1

    def __init__(self, value_obj, sys_params, internal_dict):
        super(UISegmentedControl_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.segments = None
        self.selected_segment = None
        self.highlighted_segment = None

        self.update()

    def update(self):
        self.segments = None
        self.selected_segment = None
        self.highlighted_segment = None
        super(UISegmentedControl_SynthProvider, self).update()

    def get_segments(self):
        if self.segments:
            return self.segments

        if self.sys_params.is_64_bit:
            offset = 0xe0
        else:
            offset = 0x78

        self.segments = self.value_obj.CreateChildAtOffset("segments",
                                                           offset,
                                                           self.sys_params.types_cache.NSArray)
        return self.segments

    def get_selected_segments(self):
        if self.selected_segment:
            return self.selected_segment

        if self.sys_params.is_64_bit:
            offset = 0xe8
        else:
            offset = 0x7c

        self.selected_segment = self.value_obj.CreateChildAtOffset("selectedSegment",
                                                                   offset,
                                                                   self.sys_params.types_cache.NSInteger)
        return self.selected_segment

    def get_highlighted_segment(self):
        if self.highlighted_segment:
            return self.highlighted_segment

        if self.sys_params.is_64_bit:
            offset = 0xd0
        else:
            offset = 0x80

        self.highlighted_segment = self.value_obj.CreateChildAtOffset("highlightedSegment",
                                                                   offset,
                                                                   self.sys_params.types_cache.NSInteger)
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
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, UISegmentedControl_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UISegmentedControl.UISegmentedControl_SummaryProvider \
                            --category UIKit \
                            UISegmentedControl")
    debugger.HandleCommand("type category enable UIKit")
