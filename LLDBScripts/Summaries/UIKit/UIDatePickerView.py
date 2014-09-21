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
import UIPickerView


class UIDatePickerView_SynthProvider(UIPickerView.UIPickerView_SynthProvider):
    # Class: _UIDatePickerView
    # Super class: UIPickerView
    # Protocols: UIPickerViewDelegate, UIPickerViewDataSource
    # Name:                                              armv7                 i386                  arm64                 x86_64
    # NSInteger _loadingDate                         180 (0x0B4) / 4       180 (0x0B4) / 4       336 (0x150) / 8       336 (0x150) / 8
    # NSDate * _userSuppliedDate                     184 (0x0B8) / 4       184 (0x0B8) / 4       344 (0x158) / 8       344 (0x158) / 8
    # NSDate * _userSuppliedMinimumDate              188 (0x0BC) / 4       188 (0x0BC) / 4       352 (0x160) / 8       352 (0x160) / 8
    # NSDate * _userSuppliedMaximumDate              192 (0x0C0) / 4       192 (0x0C0) / 4       360 (0x168) / 8       360 (0x168) / 8
    # NSLocale * _compositeLocale                    196 (0x0C4) / 4       196 (0x0C4) / 4       368 (0x170) / 8       368 (0x170) / 8
    # NSLocale * _userProvidedLocale                 200 (0x0C8) / 4       200 (0x0C8) / 4       376 (0x178) / 8       376 (0x178) / 8
    # NSCalendar * _userProvidedCalendar             204 (0x0CC) / 4       204 (0x0CC) / 4       384 (0x180) / 8       384 (0x180) / 8
    # NSDate * _minimumDate                          208 (0x0D0) / 4       208 (0x0D0) / 4       392 (0x188) / 8       392 (0x188) / 8
    # NSDate * _maximumDate                          212 (0x0D4) / 4       212 (0x0D4) / 4       400 (0x190) / 8       400 (0x190) / 8
    # NSDateComponents * _lastSelectedDateComponents 216 (0x0D8) / 4       216 (0x0D8) / 4       408 (0x198) / 8       408 (0x198) / 8
    # BOOL _allowsZeroTimeInterval                   220 (0x0DC) / 1  + 3  220 (0x0DC) / 1  + 3  416 (0x1A0) / 1  + 7  416 (0x1A0) / 1  + 7
    # _UIDatePickerMode * _mode                      224 (0x0E0) / 4       224 (0x0E0) / 4       424 (0x1A8) / 8       424 (0x1A8) / 8
    # NSTimeZone * _timeZone                         228 (0x0E4) / 4       228 (0x0E4) / 4       432 (0x1B0) / 8       432 (0x1B0) / 8
    # double _timeInterval                           232 (0x0E8) / 8       232 (0x0E8) / 8       440 (0x1B8) / 8       440 (0x1B8) / 8
    # UILabel * _hourLabel                           240 (0x0F0) / 4       240 (0x0F0) / 4       448 (0x1C0) / 8       448 (0x1C0) / 8
    # UILabel * _minuteLabel                         244 (0x0F4) / 4       244 (0x0F4) / 4       456 (0x1C8) / 8       456 (0x1C8) / 8
    # UIDatePicker * _datePickerDelegate             248 (0x0F8) / 4       248 (0x0F8) / 4       464 (0x1D0) / 8       464 (0x1D0) / 8
    # id _delegateOfDatePicker                       252 (0x0FC) / 4       252 (0x0FC) / 4       472 (0x1D8) / 8       472 (0x1D8) / 8
    # int _expectedAMPM                              256 (0x100) / 4       256 (0x100) / 4       480 (0x1E0) / 4       480 (0x1E0) / 4
    # struct {
    #         unsigned int staggerTimeIntervals:1;
    #         unsigned int loadingDateOrTime:1;
    #         unsigned int highlightsToday:1;
    #         unsigned int usesBlackChrome:1;
    #     } _datePickerFlags                         260 (0x104) / 1       260 (0x104) / 4       484 (0x1E4) / 4       484 (0x1E4) / 4

    def __init__(self, value_obj, internal_dict):
        super(UIDatePickerView_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "_UIDatePickerView"

        self.date = None
        self.min_user_date = None
        self.max_user_date = None
        self.min_date = None
        self.max_date = None
        self.date_components = None

    @Helpers.save_parameter("date")
    def get_date(self):
        return self.get_child_value("_userSuppliedDate")

    def get_date_value(self):
        return self.get_summary_value(self.get_date())

    def get_date_summary(self):
        date_value = self.get_date_value()
        return None if date_value is None else "date={}".format(date_value)

    @Helpers.save_parameter("min_user_date")
    def get_min_user_date(self):
        return self.get_child_value("_userSuppliedMinimumDate")

    def get_min_user_date_value(self):
        return self.get_summary_value(self.get_min_user_date())

    def get_min_user_date_summary(self):
        min_user_date_value = self.get_min_user_date_value()
        return None if min_user_date_value is None else "minDate={}".format(min_user_date_value)

    @Helpers.save_parameter("max_user_date")
    def get_max_user_date(self):
        return self.get_child_value("_userSuppliedMaximumDate")

    def get_max_user_date_value(self):
        return self.get_summary_value(self.get_max_user_date())

    def get_max_user_date_summary(self):
        max_user_date_value = self.get_max_user_date_value()
        return None if max_user_date_value is None else "maxDate={}".format(max_user_date_value)

    @Helpers.save_parameter("min_date")
    def get_min_date(self):
        return self.get_child_value("_minimumDate")

    def get_min_date_value(self):
        return self.get_summary_value(self.get_min_date())

    def get_min_date_summary(self):
        min_date_value = self.get_min_date_value()
        return None if min_date_value is None else "minDate={}".format(min_date_value)

    @Helpers.save_parameter("max_date")
    def get_max_date(self):
        return self.get_child_value("_maximumDate")

    def get_max_date_value(self):
        return self.get_summary_value(self.get_max_user_date())

    def get_max_date_summary(self):
        max_date_value = self.get_max_date_value()
        return None if max_date_value is None else "maxDate={}".format(max_date_value)

    @Helpers.save_parameter("date_components")
    def get_date_components(self):
        return self.get_child_value("_lastSelectedDateComponents")

    def get_date_components_value(self):
        return self.get_summary_value(self.get_date_components())

    def get_date_components_summary(self):
        date_components_value = self.get_date_components_value()
        return None if date_components_value is None else "{}".format(date_components_value)

    def summary(self):
        # date_summary = self.get_date_summary()
        # min_user_date_summary = self.get_min_user_date_summary()
        # max_user_date_summary = self.get_max_user_date_summary()
        # min_date_summary = self.get_min_date_summary()
        # max_date_summary = self.get_max_date_summary()

        date_components_summary = self.get_date_components_summary()

        # Summaries
        summaries = []
        # if date_value:
        #     summaries.append(date_summary)
        # if min_user_date_value:
        #     summaries.append(min_user_date_summary)
        # if max_user_date_value:
        #     summaries.append(max_user_date_summary)
        if date_components_summary:
            summaries.append(date_components_summary)

        summary = ", ".join(summaries)
        return summary


def UIDatePickerView_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIDatePickerView_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIDatePickerView.UIDatePickerView_SummaryProvider \
                            --category UIKit \
                            _UIDatePickerView")
    debugger.HandleCommand("type category enable UIKit")
