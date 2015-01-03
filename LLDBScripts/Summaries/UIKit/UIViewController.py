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
import UIResponder


class UIViewController_SynthProvider(UIResponder.UIResponder_SynthProvider):
    def __init__(self, value_obj, internal_dict):
        super(UIViewController_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIViewController"

        self.title = None

    @Helpers.save_parameter("title")
    def get_title(self):
        return self.get_child_value("_title")

    def get_title_value(self):
        return SummaryBase.get_summary_value(self.get_title())

    def get_title_summary(self):
        title_value = self.get_title_value()
        return None if title_value is None else "title={}".format(title_value)

    def summary(self):
        title_summary = self.get_title_summary()

        summaries = []
        if title_summary:
            summaries.append(title_summary)

        summary = ", ".join(summaries)
        return summary


def UIViewController_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIViewController_SynthProvider)


def __lldb_init_module(debugger, dictionary):
    debugger.HandleCommand("type summary add -F UIViewController.UIViewController_SummaryProvider \
                            --category UIKit \
                            UIViewController")
    debugger.HandleCommand("type category enable UIKit")
