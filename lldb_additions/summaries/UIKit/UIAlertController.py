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
import UIViewController

UIAlertControllerStyleActionSheet = 0
UIAlertControllerStyleAlert = 1


def get_style_name(value):
        name = "Unknown"
        if value == 0:
            name = "ActionSheet"
        elif value == 1:
            name = "Alert"
        return name


class UIAlertControllerSyntheticProvider(UIViewController.UIViewControllerSyntheticProvider):
    """
    Class representing UIAlertController.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIAlertControllerSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIAlertController"

        self.register_child_value("message", ivar_name="_message",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_message_summary)
        self.register_child_value("attributed_title", ivar_name="_attributedTitle",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_attributed_title_summary)
        self.register_child_value("attributed_message", ivar_name="_attributedMessage",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_attributed_message_summary)
        self.register_child_value("actions", ivar_name="_actions",
                                  primitive_value_function=SummaryBase.get_count_value,
                                  summary_function=self.get_actions_summary)
        self.register_child_value("resolved_style", ivar_name="_resolvedStyle",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_resolved_style_summary)
        self.register_child_value("preferred_style", ivar_name="_preferredStyle",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_preferred_style_summary)

    @staticmethod
    def get_message_summary(value):
        return "message={}".format(value)

    @staticmethod
    def get_attributed_title_summary(value):
        return "title={}".format(value)

    @staticmethod
    def get_attributed_message_summary(value):
        return "attributedMessage={}".format(value)

    @staticmethod
    def get_actions_summary(value):
        return "actions={}".format(value)

    @staticmethod
    def get_resolved_style_summary(value):
        name = get_style_name(value)
        return "resolvedStyle={}".format(name)

    @staticmethod
    def get_preferred_style_summary(value):
        name = get_style_name(value)
        return "preferredStyle={}".format(name)

    def summary(self):
        summary = SummaryBase.join_summaries(self.title_summary, self.message_summary,
                                             self.preferred_style_summary, self.actions_summary)
        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UIAlertControllerSyntheticProvider)
