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
import UIControl
import UILabel


class UIButton_SynthProvider(UIControl.UIControl_SynthProvider):
    def __init__(self, value_obj, internal_dict):
        super(UIButton_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIButton"

        self.label = None
        self.label_provider = None

    @Helpers.save_parameter("label")
    def get_label(self):
        return self.get_child_value("_titleView")

    @Helpers.save_parameter("label_provider")
    def get_label_provider(self):
        label = self.get_label()
        return None if label is None else UILabel.UILabel_SynthProvider(label, self.internal_dict)

    def get_label_value(self):
        label_provider = self.get_label_provider()
        return None if label_provider is None else label_provider.get_text_value()

    def get_label_summary(self):
        label_value = self.get_label_value()
        return None if label_value is None else "text={}".format(self.get_label_value())

    def summary(self):
        label_summary = self.get_label_summary()
        tag_summary = self.get_tag_summary()

        summaries = []
        if label_summary:
            summaries.append(label_summary)
        if self.get_tag_value() != 0:
            summaries.append(tag_summary)

        summary = ", ".join(summaries)
        return summary


def UIButton_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIButton_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIButton.UIButton_SummaryProvider \
                            --category UIKit \
                            UIButton")
    debugger.HandleCommand("type category enable UIKit")
