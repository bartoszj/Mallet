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

from ...scripts import helpers
from .. import SummaryBase
import UIControl
import UILabel


class UITextFieldSyntheticProvider(UIControl.UIControlSyntheticProvider):
    """
    Class representing UITextField.
    """
    def __init__(self, value_obj, internal_dict):
        super(UITextFieldSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UITextField"

        self.register_child_value("display_label", ivar_name="_displayLabel",
                                  provider_class=UILabel.UILabelSyntheticProvider,
                                  summary_function=self.get_display_label_summary)
        self.register_child_value("placeholder_label", ivar_name="_placeholderLabel",
                                  provider_class=UILabel.UILabelSyntheticProvider,
                                  summary_function=self.get_placeholder_label_summary)

    @staticmethod
    def get_display_label_summary(provider):
        """
        Display label summary.

        :param UILabel.UILabelSyntheticProvider provider: Label provider.
        :return: Display label summary.
        :rtype: str
        """
        value = provider.text_value
        if value is not None:
            return "text={}".format(value)
        return None

    @staticmethod
    def get_placeholder_label_summary(provider):
        """
        Placeholder label summary.

        :param UILabel.UILabelSyntheticProvider provider: Label provider.
        :return: Placeholder label summary.
        :rtype: str
        """
        value = provider.text_value
        if value is not None:
            return "placeholder={}".format(value)
        return None

    def summary(self):
        summary = SummaryBase.join_summaries(self.display_label_summary, self.placeholder_label_summary)
        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UITextFieldSyntheticProvider)
