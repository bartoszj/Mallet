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


class UIPageControl_SynthProvider(UIControl.UIControl_SynthProvider):
    # Class: UIPageControl
    # Super class: UIControl
    # Name:                                                armv7                 i386                  arm64                 x86_64
    # NSMutableArray * _indicators                     120 (0x078) / 4       120 (0x078) / 4       224 (0x0E0) / 8       224 (0x0E0) / 8
    # NSInteger _currentPage                           124 (0x07C) / 4       124 (0x07C) / 4       232 (0x0E8) / 8       232 (0x0E8) / 8
    # NSInteger _displayedPage                         128 (0x080) / 4       128 (0x080) / 4       240 (0x0F0) / 8       240 (0x0F0) / 8
    # struct {
    #         unsigned int hideForSinglePage:1;
    #         unsigned int defersCurrentPageDisplay:1;
    #     } _pageControlFlags                          132 (0x084) / 1  + 3  132 (0x084) / 4       248 (0x0F8) / 4  + 4  248 (0x0F8) / 4  + 4
    # UIImage * _currentPageImage                      136 (0x088) / 4       136 (0x088) / 4       256 (0x100) / 8       256 (0x100) / 8
    # UIImage * _pageImage                             140 (0x08C) / 4       140 (0x08C) / 4       264 (0x108) / 8       264 (0x108) / 8
    # NSInteger _lastUserInterfaceIdiom                144 (0x090) / 4       144 (0x090) / 4       272 (0x110) / 8       272 (0x110) / 8
    # UIColor * _currentPageIndicatorTintColor         148 (0x094) / 4       148 (0x094) / 4       280 (0x118) / 8       280 (0x118) / 8
    # UIColor * _pageIndicatorTintColor                152 (0x098) / 4       152 (0x098) / 4       288 (0x120) / 8       288 (0x120) / 8
    # _UILegibilitySettings * _legibilitySettings      156 (0x09C) / 4       156 (0x09C) / 4       296 (0x128) / 8       296 (0x128) / 8

    def __init__(self, value_obj,internal_dict):
        super(UIPageControl_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIPageControl"

        self.indicators = None
        self.current_page = None
        self.displayed_page = None

    def get_indicators(self):
        if self.indicators:
            return self.indicators

        self.indicators = self.get_child_value("_indicators")
        return self.indicators

    def get_indicators_value(self):
        return self.get_count_value(self.get_indicators())

    def get_indicators_summary(self):
        indicators_value = self.get_indicators_value()
        if indicators_value is None:
            return None
        return "numberOfPages={}".format(indicators_value)

    def get_current_page(self):
        if self.current_page:
            return self.current_page

        self.current_page = self.get_child_value("_currentPage")
        return self.current_page

    def get_current_page_value(self):
        return self.get_signed_value(self.get_current_page())

    def get_current_page_summary(self):
        current_page_value = self.get_current_page_value()
        if current_page_value is None:
            return None
        return "currentPage={}".format(current_page_value)

    def get_displayed_page(self):
        if self.displayed_page:
            return self.displayed_page

        self.displayed_page = self.get_child_value("_displayedPage")
        return self.displayed_page

    def get_displayed_page_value(self):
        return self.get_signed_value(self.get_displayed_page())

    def get_displayed_page_summary(self):
        displayed_page_value = self.get_displayed_page_value()
        if displayed_page_value is None:
            return None
        return "displayedPage={}".format(displayed_page_value)

    def summary(self):
        indicators_summary = self.get_indicators_summary()
        current_page_summary = self.get_current_page_summary()
        # displayed_page_summary = self.get_displayed_page_summary()

        # Summaries
        summaries = [current_page_summary, indicators_summary]

        summary = ", ".join(summaries)
        return summary


def UIPageControl_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIPageControl_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIPageControl.UIPageControl_SummaryProvider \
                            --category UIKit \
                            UIPageControl")
    debugger.HandleCommand("type category enable UIKit")
