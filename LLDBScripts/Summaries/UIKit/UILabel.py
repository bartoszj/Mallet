#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2013 Bartosz Janda
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
import UIView


class UILabel_SynthProvider(UIView.UIView_SynthProvider):
    def __init__(self, value_obj, internal_dict):
        super(UILabel_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UILabel"

        self.text = None

    @Helpers.save_parameter("text")
    def get_text(self):
        return self.get_child_value("_content", "NSAttributedString *")

    def get_text_value(self):
        return SummaryBase.get_summary_value(self.get_text())

    def get_text_summary(self):
        text_value = self.get_text_value()
        return None if text_value is None else "text={}".format(text_value)

    def summary(self):
        text_summary = self.get_text_summary()
        tag_summary = self.get_tag_summary()

        summaries = []
        if text_summary:
            summaries.append(text_summary)
        if self.get_tag_value() != 0:
            summaries.append(tag_summary)

        summary = ", ".join(summaries)
        return summary


def UILabel_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UILabel_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UILabel.UILabel_SummaryProvider \
                            --category UIKit \
                            UILabel")
    debugger.HandleCommand("type category enable UIKit")
