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


class UIButtonSyntheticProvider(UIControl.UIControlSyntheticProvider):
    """
    Class representing UIButton.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIButtonSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIButton"

        self.register_child_value("label", ivar_name="_titleView",
                                  provider_class=UILabel.UILabelSyntheticProvider,
                                  summary_function=self.get_label_summary)

    @staticmethod
    def get_label_summary(provider):
        """
        UILabel summary.

        :param UILabel.UILabelSyntheticProvider provider: UILabel provider.
        :return: UILabel summary.
        :rtype: str
        """
        return "text={}".format(provider.text_value)

    def summary(self):
        summary = SummaryBase.join_summaries(self.label_summary, self.tag_summary)
        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UIButtonSyntheticProvider)


def __lldb_init_module(debugger, dictionary):
    debugger.HandleCommand("type summary add -F UIButton.summary_provider \
                            --category UIKit \
                            UIButton")
    debugger.HandleCommand("type category enable UIKit")
