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


class UIPageControl_SynthProvider(UIControl.UIControl_SynthProvider):
    # UIPageControl:
    # Offset / size (+ alignment)                                           32bit:                  64bit:
    #
    # NSMutableArray *_indicators                                           120 = 0x78 / 4          224 = 0xe0 / 8
    # NSInteger _currentPage                                                124 = 0x7c / 4          232 = 0xe8 / 8
    # NSInteger _displayedPage                                              128 = 0x80 / 4          240 = 0xf0 / 8
    # struct {
    #     unsigned int hideForSinglePage:1;
    #     unsigned int defersCurrentPageDisplay:1;
    # } _pageControlFlags                                                   132 = 0x84 / 1 + 3      248 = 0xf8 / 1  +7
    # UIImage *_currentPageImage                                            136 = 0x88 / 4          256 = 0x100 / 8
    # UIImage *_pageImage                                                   140 = 0x8c / 4          264 = 0x108 / 8
    # NSInteger _lastUserInterfaceIdiom                                     144 = 0x90 / 4          272 = 0x110 / 8
    # UIColor *_currentPageIndicatorTintColor                               148 = 0x94 / 4          280 = 0x118 / 8
    # UIColor *_pageIndicatorTintColor                                      152 = 0x98 / 4          288 = 0x120 / 8
    # _UILegibilitySettings *_legibilitySettings                            156 = 0x9c / 4          296 = 0x128 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        super(UIPageControl_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.indicators = None
        self.current_page = None
        self.displayed_page = None

        self.update()

    def update(self):
        self.indicators = None
        self.current_page = None
        self.displayed_page = None
        super(UIPageControl_SynthProvider, self).update()

    def get_indicators(self):
        if self.indicators:
            return self.indicators

        if self.sys_params.is_64_bit:
            offset = 0xe0
        else:
            offset = 0x78

        self.indicators = self.value_obj.CreateChildAtOffset("indicators",
                                                             offset,
                                                             self.sys_params.types_cache.NSArray)
        return self.indicators

    def get_current_page(self):
        if self.current_page:
            return self.current_page

        if self.sys_params.is_64_bit:
            offset = 0xe8
        else:
            offset = 0x7c

        self.current_page = self.value_obj.CreateChildAtOffset("currentPage",
                                                               offset,
                                                               self.sys_params.types_cache.NSInteger)
        return self.current_page

    def get_displayed_page(self):
        if self.displayed_page:
            return self.displayed_page

        if self.sys_params.is_64_bit:
            offset = 0xf0
        else:
            offset = 0x80

        self.displayed_page = self.value_obj.CreateChildAtOffset("displayPage",
                                                                 offset,
                                                                 self.sys_params.types_cache.NSInteger)
        return self.displayed_page

    def summary(self):
        indicators = self.get_indicators()
        indicators_value = indicators.GetNumChildren()
        indicators_summary = "numberOfPages={}".format(indicators_value)

        current_page = self.get_current_page()
        current_page_value = current_page.GetValueAsSigned()
        current_page_summary = "currentPage={}".format(current_page_value)

        # displayed_page = self.get_displayed_page()
        # displayed_page_value = displayed_page.GetValueAsSigned()
        # displayed_page_summary = "displayedPage={}".format(displayed_page_value)

        # Summaries
        summaries = [current_page_summary, indicators_summary]

        summary = ", ".join(summaries)
        return summary


def UIPageControl_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, UIPageControl_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIPageControl.UIPageControl_SummaryProvider \
                            --category UIKit \
                            UIPageControl")
    debugger.HandleCommand("type category enable UIKit")
