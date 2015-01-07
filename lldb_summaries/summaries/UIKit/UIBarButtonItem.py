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

from ...scripts import helpers
from .. import SummaryBase
from ..Foundation import NSObject


class UIBarButtonItemSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing UIBarButtonItem.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIBarButtonItemSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIBarButtonItem"

        self.register_child_value("title", ivar_name="_title",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_title_summary)
        self.register_child_value("width", ivar_name="_width",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_width_summary)

    @staticmethod
    def get_title_summary(value):
        return "title={}".format(value)

    @staticmethod
    def get_width_summary(value):
        if value != 0:
            return "width={}".format(SummaryBase.formatted_float(value))
        return None

    def summary(self):
        summary = SummaryBase.join_summaries(self.title_summary, self.width_summary)
        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UIBarButtonItemSyntheticProvider)


def __lldb_init_module(debugger, dictionary):
    debugger.HandleCommand("type summary add -F UIBarButtonItem.summary_provider \
                            --category UIKit \
                            UIBarButtonItem")
    debugger.HandleCommand("type category enable UIKit")