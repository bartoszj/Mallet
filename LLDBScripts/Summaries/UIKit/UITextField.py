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


class UITextField_SynthProvider(UIControl.UIControl_SynthProvider):
    def __init__(self, value_obj, internal_dict):
        super(UITextField_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UITextField"

        self.display_label = None
        self.display_label_provider = None
        self.placeholder_label = None
        self.placeholder_label_provider = None

    @Helpers.save_parameter("display_label")
    def get_display_label(self):
        return self.get_child_value("_displayLabel")

    @Helpers.save_parameter("display_label_provider")
    def get_display_label_provider(self):
        display_label = self.get_display_label()
        return None if display_label is None else UILabel.UILabel_SynthProvider(display_label, self.internal_dict)

    def get_display_label_text(self):
        display_label_provider = self.get_display_label_provider()
        return None if display_label_provider is None else display_label_provider.get_text()

    def get_display_label_text_value(self):
        return self.get_summary_value(self.get_display_label_text())

    def get_display_label_text_summary(self):
        display_label_text_value = self.get_display_label_text_value()
        return None if display_label_text_value is None else "text={}".format(display_label_text_value)

    @Helpers.save_parameter("placeholder_label")
    def get_placeholder_label(self):
        return self.get_child_value("_placeholderLabel")

    @Helpers.save_parameter("placeholder_label_provider")
    def get_placeholder_label_provider(self):
        placeholder_label = self.get_placeholder_label()
        return None if placeholder_label is None else UILabel.UILabel_SynthProvider(placeholder_label, self.internal_dict)

    def get_placeholder_label_text(self):
        placeholder_label_provider = self.get_placeholder_label_provider()
        return None if placeholder_label_provider is None else placeholder_label_provider.get_text()

    def get_placeholder_label_text_value(self):
        return self.get_summary_value(self.get_placeholder_label_text())

    def get_placeholder_label_text_summary(self):
        placeholder_label_text_value = self.get_placeholder_label_text_value()
        return None if placeholder_label_text_value is None else "placeholder={}".format(placeholder_label_text_value)

    def summary(self):
        display_label_text_summary = self.get_display_label_text_summary()
        placeholder_label_text_summary = self.get_placeholder_label_text_summary()

        # Summary
        summaries = []
        if display_label_text_summary:
            summaries.append(display_label_text_summary)
        if placeholder_label_text_summary:
            summaries.append(placeholder_label_text_summary)

        summary = ", ".join(summaries)
        return summary


def UITextField_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UITextField_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UITextField.UITextField_SummaryProvider \
                            --category UIKit \
                            UITextField")
    debugger.HandleCommand("type category enable UIKit")
