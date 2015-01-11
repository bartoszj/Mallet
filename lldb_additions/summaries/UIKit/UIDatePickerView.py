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

from ...scripts import helpers
from .. import SummaryBase
import UIPickerView


class UIDatePickerViewSyntheticProvider(UIPickerView.UIPickerViewSyntheticProvider):
    """
    Class representing _UIDatePickerView.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIDatePickerViewSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "_UIDatePickerView"

        self.register_child_value("date", ivar_name="_userSuppliedDate",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_date_summary)
        self.register_child_value("min_user_date", ivar_name="_userSuppliedMinimumDate",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_min_user_date_summary)
        self.register_child_value("max_user_date", ivar_name="_userSuppliedMaximumDate",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_max_user_date_summary)
        self.register_child_value("min_date", ivar_name="_minimumDate",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_min_date_summary)
        self.register_child_value("max_date", ivar_name="_maximumDate",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_max_date_summary)
        self.register_child_value("date_components", ivar_name="_lastSelectedDateComponents",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_date_components_summary)

    @staticmethod
    def get_date_summary(value):
        return "date={}".format(value)

    @staticmethod
    def get_min_user_date_summary(value):
        return "minDate={}".format(value)

    @staticmethod
    def get_max_user_date_summary(value):
        return "maxDate={}".format(value)

    @staticmethod
    def get_min_date_summary(value):
        return "minDate={}".format(value)

    @staticmethod
    def get_max_date_summary(value):
        return "maxDate={}".format(value)

    @staticmethod
    def get_date_components_summary(value):
        return "{}".format(value)

    def summary(self):
        return self.date_components_summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UIDatePickerViewSyntheticProvider)


def lldb_init(debugger, dictionary):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                            --category UIKit \
                            _UIDatePickerView".format(__name__))
    debugger.HandleCommand("type category enable UIKit")
