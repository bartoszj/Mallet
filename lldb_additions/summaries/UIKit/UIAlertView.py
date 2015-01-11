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
import UIView
import UIAlertController

UIAlertViewStyleDefault = 0
UIAlertViewStyleSecureTextInput = 1
UIAlertViewStylePlainTextInput = 2
UIAlertViewStyleLoginAndPasswordInput = 3


def get_alert_view_style_name(value):
    name = "Unknown"
    if value == 0:
        name = "Default"
    elif value == 1:
        name = "SecureTextInput"
    elif value == 2:
        name = "PlainTextInput"
    elif value == 3:
        name = "LoginAndPasswordInput"
    return name


class UIAlertViewSyntheticProvider(UIView.UIViewSyntheticProvider):
    """
    Class representing UIAlertView.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIAlertViewSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIAlertView"

        self.register_child_value("alert_controller", ivar_name="_alertController",
                                  provider_class=UIAlertController.UIAlertControllerSyntheticProvider,
                                  summary_function=self.get_alert_controller_summary)
        self.register_child_value("actions", ivar_name="_actions",
                                  primitive_value_function=SummaryBase.get_count_value,
                                  summary_function=self.get_actions_summary)
        self.register_child_value("message", ivar_name="_message",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_message_summary)
        self.register_child_value("subtitle", ivar_name="_subtitle",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_subtitle_summary)
        self.register_child_value("alert_view_style", ivar_name="_alertViewStyle",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_alert_view_style_summary)

    @staticmethod
    def get_alert_controller_summary(provider):
        """
        UIAlertController summary.

        :param UIAlertController.UIAlertControllerSyntheticProvider provider: UIAlertController provider.
        :return: UIAlertController summary.
        :rtype: str
        """
        return provider.summary()

    @staticmethod
    def get_actions_summary(value):
        return "actions={}".format(value)

    @staticmethod
    def get_message_summary(value):
        return "message={}".format(value)

    @staticmethod
    def get_subtitle_summary(value):
        return "subtitle={}".format(value)

    @staticmethod
    def get_alert_view_style_summary(value):
        return "style={}".format(get_alert_view_style_name(value))

    def get_title_summary(self):
        return self.alert_controller_provider.title_summary

    def summary(self):
        summary = SummaryBase.join_summaries(self.get_title_summary(), self.message_summary, self.alert_view_style_summary)
        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UIAlertViewSyntheticProvider)


def lldb_init(debugger, dictionary):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                            --category UIKit \
                            UIAlertView".format(__name__))
    debugger.HandleCommand("type category enable UIKit")
