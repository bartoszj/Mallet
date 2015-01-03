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


class UIPageControl_SynthProvider(UIControl.UIControl_SynthProvider):
    def __init__(self, value_obj, internal_dict):
        super(UIPageControl_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIPageControl"

        self.indicators = None
        self.current_page = None
        self.displayed_page = None

    @Helpers.save_parameter("indicators")
    def get_indicators(self):
        return self.get_child_value("_indicators")

    def get_indicators_value(self):
        return SummaryBase.get_count_value(self.get_indicators())

    def get_indicators_summary(self):
        indicators_value = self.get_indicators_value()
        return None if indicators_value is None else "numberOfPages={}".format(indicators_value)

    @Helpers.save_parameter("current_page")
    def get_current_page(self):
        return self.get_child_value("_currentPage")

    def get_current_page_value(self):
        return SummaryBase.get_signed_value(self.get_current_page())

    def get_current_page_summary(self):
        current_page_value = self.get_current_page_value()
        return None if current_page_value is None else "currentPage={}".format(current_page_value)

    @Helpers.save_parameter("displayed_page")
    def get_displayed_page(self):
        return self.get_child_value("_displayedPage")

    def get_displayed_page_value(self):
        return SummaryBase.get_signed_value(self.get_displayed_page())

    def get_displayed_page_summary(self):
        displayed_page_value = self.get_displayed_page_value()
        return None if displayed_page_value is None else "displayedPage={}".format(displayed_page_value)

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
